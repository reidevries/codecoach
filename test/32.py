#! /usr/bin/env python2.6
import sys
import string

argv = len(sys.argv)

if argv != 2:
	sys.exit(1)
	
	
argo = sys.argv[1]

if str.isdigit(argo):
	number = int(argo)
	if number > 7:
		print "High Value"
	elif number < 7:
		print "Low Value"
	else:
		print "Neither"
else:
	print "Neither"

	
sys.exit(0)