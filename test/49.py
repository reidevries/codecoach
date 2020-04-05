#! /usr/bin/env python2.6

import sys
import os

argv = len(sys.argv)
if argv != 2:
	print "Usage: Parse.py <filename>;"
	sys.exit(1)
	
argo = sys.argv[1]

try:
	InFile = open(argo, "r")
except:
	print argo,"is not a readable file."

for line in InFile:
	line = line.split()
	length = len(line)
	length = range(length)
	strings = []
	summation = 0.0
	count = 0.0
	average = 0.0
	for I in length:
		try:
			number = int(line[I])
		except:
			strings.append(line[I])
		else:
			summation += number
			count += 1
	if count != 0:
		average = summation / count
		print"%.3f" % (average),
	for I in range(len(strings)):
		print strings[I],
	print
