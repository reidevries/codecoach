#! /usr/bin/env python2.6

import sys

argv = len(sys.argv)

if argv != 2:
	sys.exit(1)
	
	
argo = sys.argv[1]
argo = int(argo)
Arr = range(argo)
sums = 0
for i in Arr:
	sums += Arr[i] + 1

print "%d" % sums

sys.exit(0)