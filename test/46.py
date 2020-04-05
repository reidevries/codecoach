#! /usr/bin/env python2.6

import sys

argv = len(sys.argv)
if argv != 3:
	print "usage: chain <region> <animal>"
	sys.exit(1)

lines=sys.stdin.readlines()
Final = []
success = 0
successplace = 0
for L in lines:
	L = L.rstrip()
	name = L.split(" ")
	Arr = name[1:]
	length = len(Arr) - 1
	length = range(length)
	Arrr=[]
	for loop in length:
		make = tuple([Arr[loop],Arr[loop+1]])
		Arrr.append(make)
		add = [name[0], Arrr]
	Final.append(add)

numberoflines = len(Final)
argo = sys.argv[1]
argo2 = sys.argv[2]
numberoflines = range(numberoflines)

winner = Final[1][0]
losing = argo

if winner == losing:
	print "Winner winner"
	
for places in numberoflines:
	print Final[places]
	if Final[places][0] == argo:
		numberofkills = len(Final[places][1])
		numberofkills = range(numberofkills)
		for kills in numberofkills:
			successplace = 1
			if Final[places][1][kills][0] == argo2:
				success = 1
				killed = Final[places][1][kills][1]
				
if success == 1:
	print
	print "In the", argo, "the", argo2, "is eaten by the", killed
elif successplace == 1:
	print
	print "In the", argo, "no", argo2, "are eaten"
else:
	print
	print "No chain entry for", argo
sys.exit(0)