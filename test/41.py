#! /usr/bin/env python2.6

import re
import sys
import os

argv = len(sys.argv)
if argv != 2:
	print "usage: ipfun.py <filename>"
	sys.exit(1)


argo = sys.argv[1]

if (os.access(argo, os.R_OK) == 0):
	print argo, "is not readable"
	sys.exit(2)

InFile = open(argo, "r")
ipcheck = r"((([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5]))\.(([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5]))\.(([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5]))\.(([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5]))\:)"

for line in InFile:
	validip = re.match(ipcheck, line)
	line = line.split('\n')
	line = line[0]
	if validip:
		line2 = line.split(':')
		try :
			port = int(line2[1])
		except:
			print line,"- Invalid Port Number"
		else:
			if ((port > 0) & (port < 32767)):
				validport = 1
				if port < 1024:
					root = 1
					print line,"- Valid (root privileges required)"
				else:
					root = 0
					print line,"- Valid"
			else:
				print line,"- Invalid Port Number"
					
	else:
		print line,"- Invalid IP Address"
	
sys.exit(0)