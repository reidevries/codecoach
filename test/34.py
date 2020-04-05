import sys
import os
import math
argv = len(sys.argv)

Cato = {}
if argv != 2:
	print "usage: sensors.py <inputfile>"
	sys.exit(1)
	
argo = sys.argv[1]

if (os.path.isfile(argo) == 0):
	print argo, "is not a readable file."
	sys.exit(1)
if (os.access(argo, os.R_OK) == 0):
	print argo, "is not a readable file."
	sys.exit(1)
	
InFile = open(argo, "r")

for line in InFile:
	splits = line.split(":")
	#print splits[0]
	name = splits[0]
	#print splits
	del splits[0]
	#print splits[0]
	numbers = splits[0].split("\n")
	#print numbers
	numbers = numbers[0].split(",")
	#print numbers
	length = len(numbers)
	length = range(length)
	
	#for I in length:
	if Cato.has_key(name):
		past = Cato.get(name)
		past.extend(numbers)
		A = {name : past}
	else:
		A = {name : numbers}
		Cato.update(A)
		#print Cato.keys()
		
#print Cato.values()
print Cato.keys()	
NAMES = Cato.keys()
length = len(NAMES)
length = range(length)
Cato.update(Cato)
for I in length:
	numbers = Cato.get(NAMES[I])
	#print numbers
	count = len(numbers)
	arrRange = range(count)
	mini = min(numbers)
	maxi = max(numbers)
	summation = 0
	for J in arrRange:
		#print numbers[J]
		summation += float(numbers[J])
	average= summation/count
	name = NAMES[I]
	print NAMES[I],": min=%.3f, max=%.3f, sum=%.3f, avg=%.3f, stdev=%.3f" % (float(mini), float(maxi), float(summation), average, 0)  
	#summation
	#print mini
	#print maxi
		
		
sys.exit(0)