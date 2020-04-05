#! /usr/bin/env python2.6

import sys

print "Please enter some values: ",
data = sys.stdin.readline()
data = data.split()
length = len(data)
length = range(length)
summation = 0.0
number = 0.0
for I in length:
	try:
		number = float(data[I])
	except:
		error=1
	else:
		summation += number
print"The sum is:",summation

sys.exit(0)