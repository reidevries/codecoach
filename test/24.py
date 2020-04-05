#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012-2013, Bartosz Foder, (bartosz@foder.pl)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import time
import urllib
import re
import wx
import wx.lib.mixins.listctrl as listmix
import os
import pickle
import threading

EVT_DU = wx.NewEventType()
EVT_DUP = wx.PyEventBinder(EVT_DU, 1)

def findList(url):
	site = urllib.urlopen(url).read()
	list = re.findall(r"\W+<li><a href=\"((?:https?://)?(?:[\da-z\.\-/\_]+))\"\s+rel=\"\d+\" class=\"(?:[a-z_]+ [a-z_]+)\">([0-9a-zA-Z\ \.\\/\-\_\+=]+)</a></li>",site)
	
	saveList(list)
	return list

def findChapters(url):
	site = urllib.urlopen(url).read()
	list = re.findall(r"<a href=\"((?:https?://)?(?:[\da-z\.\-/\_]+))\"\s+title=\"(?:[A-Za-z0-9\s\\/\-\_!@,\.\*\+]+)\"\s+class=\"tips\">([A-Za-z0-9\s\\/\-\_!@,\.\*\+]+)\s*</a>",site)

	list.reverse()
	return list

def findPages(url):
	site = urllib.urlopen(url).read()
	dirurl = url[:url.rfind('/')]
	site = site[:site.index(r'btn next_page')]

	pageslist = re.findall(r"option\svalue=\"(\w+)\"",site)
	pageurls = [dirurl+'/'+x+'.htm' for x in pageslist if int(x)>0]
	return pageurls

def findImage(url):
	site = urllib.urlopen(url).read()
	imageurl = re.search(r"onclick=\"return enlarge\(\)\"><img src=\"((https?://)?([\da-zA-Z\.\-/\_]+))\"",site)
	
	if imageurl is not None: return imageurl.group(1)
	return None


def saveList(list):
	pickle.dump(list,open('manga.db','w'))


class sf(wx.Frame):
	def __init__(self,parent):
		wx.Frame.__init__(self, parent, title="MFD",size=(800,600))
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		list = self.readList()		
		self.MangaListCB = wx.ComboBox(self,choices=[x[1] for x in list],value=list[0][1],style=wx.CB_READONLY,validator=wx.DefaultValidator)		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		
		hbox.Add(self.MangaListCB,flag=wx.EXPAND|wx.RIGHT,border=8,proportion=1)
		
		refbtn = wx.Button(self,label='Refresh List')
		hbox.Add(refbtn,flag=wx.EXPAND)
		vbox.Add(hbox,flag=wx.ALL,border=5)

		titlebtn = wx.Button(self,label='Get list of Chapters')
		vbox.Add(titlebtn,flag=wx.EXPAND|wx.ALL,border=5)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.ChaptersLB = wx.CheckListBox(self,style=wx.LC_REPORT,size=(800,400))
		selall = wx.Button(self, label='Select All')
		
		
		hbox.Add(self.ChaptersLB,flag=wx.EXPAND|wx.ALL,border=5,proportion=0)
		hbox.Add(selall,flag=wx.EXPAND|wx.ALL,border=5,proportion=0)
		
		vbox.Add(hbox,flag=wx.ALL,border=5)

		downlbtn = wx.Button(self, label='Download Chapters')
		vbox.Add(downlbtn,flag=wx.EXPAND|wx.ALL,border=5)
		
		self.Bind(EVT_DUP,self.updateProgress)
		self.Bind(wx.EVT_BUTTON,self.downloadChapters,downlbtn)
		self.Bind(wx.EVT_BUTTON,self.getChapters,titlebtn)
		self.Bind(wx.EVT_BUTTON,self.refresh,refbtn)
		self.Bind(wx.EVT_BUTTON,self.selectAll,selall)

		self.SetSizerAndFit(vbox)
		self.SetAutoLayout(True)
		self.Centre()
		self.Show(True)

	def downloadChapters(self,event):
		chaptersurls = [(self.chapters[sel][0],self.chapters[sel][1]) for sel in self.ChaptersLB.GetChecked()]
		
		worker = DownloadThread(self,chaptersurls)
		worker.start()

	def readList(self):
		if not os.path.exists('manga.db'): return findList('http://mangafox.me/manga/')
		
		return pickle.load(open('manga.db','r'))

	def refresh(self,event):
		list = findList('http://mangafox.me/manga/')
		self.MangaListCB.Items = [x[1] for x in list]
		self.MangaListCB.Select(0)

	def getChapters(self,event):
		list = self.readList()

		churl = None
		ci = self.MangaListCB.GetValue()
		
		for x in list:
			if x[1] == ci: churl = x[0]
		if churl is None: return

		self.chapters = findChapters(churl)
		self.ChaptersLB.Set([ch[1]+'\t('+ch[0]+')'for ch in self.chapters])
	
	def selectAll(self,evt):
		self.ChaptersLB.SetChecked(range(self.ChaptersLB.GetCount()))
	
	def updateProgress(self,evt):
		print evt.GetValue()
		

class DownloadUpdateEvent(wx.PyCommandEvent):
	def __init__(self, etype, eid, value=None):
		wx.PyCommandEvent.__init__(self, etype, eid)
		self._value = value
		
	def GetValue(self):
		return self._value

class DownloadThread(threading.Thread):
	def __init__(self,parent,urls):
		threading.Thread.__init__(self)
		
		self.chapters = urls
		self._parent = parent
		
	def run(self):
		print self.chapters
		if not os.path.exists("./manga/"): os.makedirs("./manga/")
		for x in self.chapters:
			path_ = "./manga/"+re.sub(r"[/\.\+]","_",x[1])
			if not os.path.exists(path_): os.makedirs(path_)
			pages = findPages(x[0])
			for page in pages:
				
				img = findImage(page)
				if img is None: continue
				
				u = urllib.urlopen(img)
				
				f = open(path_+'/'+page.split('/')[-1].replace('htm','jpg'),'wb')
				f.write(u.read())
				f.close()
				
				evt = DownloadUpdateEvent(EVT_DU, -1, value = 'Chapter: '+str(self.chapters.index(x)+1)+'/'+str(len(self.chapters))+' Page: '+str(pages.index(page)+1)+'/'+str(len(pages)))
				wx.PostEvent(self._parent, evt)
		evt = DownloadUpdateEvent(EVT_DU, -1, value = 'Done :)')
		wx.PostEvent(self._parent, evt)

if __name__ == '__main__':
	app = wx.App(False)
	w = sf(None)
	app.MainLoop()
