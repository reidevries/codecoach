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

for line in InFile:
	funct = re.match(functionline, line)
	if funct:
		Cato = funct.groupdict()
		print Cato['FunctionName']
		args = Cato['Args']
		args = args.split(',')
		argnum = 1
		for I in args:
			out=""
			out += 'Arg'
			out += str(argnum)
			out += ':'
			print out,I
			argnum += 1
			
			
		
sys.exit(0)
	