__author__ = 'zimoshe-AT-gmail.com (Moshe Zioni, aka dalmoz)'

from sys import argv
#import pprint # PDEBUG
import json

from apiclient.discovery import build


def main():
  service = build("customsearch", "v1",
			developerKey="enterYours") #ome

  #print argv[1]
  #proto typez=['asp','aspx','jsp','java','php','rb','py','pdf','old','back','bak','bac','tmp']
  typez=['asp','aspx','jsp','java','pdf','old','back','bak','bac','tmp']
  suffz=['1','2','3','4','5','6','7','8','9','11','old','back','bac','bak','tmp','temp']
  for t in typez:
	filetype = ''
	for s in suffz:
		  filetype += 'filetype:' + str(t) + str(s) + ' OR '
	filetype=filetype[:-4] # last OR is disturbing the force
	#print "SEARCH: " + filetype # PRDEBUG
	res = service.cse().list(
	 q=filetype,
	 #cx is wng token
	 cx='017840724651753821015:nrkcgipytkk', 
	  ).execute()
		  #print str(sys.argv)
		  #print(json.dumps(res['searchInformation', ['totalResults']], indent=1))
	try:
	  #print filetype
	  print(json.dumps([s['link'] for s in res['items']], indent=1))
	except:
	  print "\tNo results on    " + str(t)
		  #print 'Link: %s' % res('link')[1]


if __name__ == '__main__':
  main()
