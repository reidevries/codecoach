#! /usr/bin/env python2.6

import sys

argv = len(sys.argv)

if argv != 2:
	sys.exit(1)
	
	
argo = sys.argv[1]
argo = int(argo) + 4
argo /=5
num = 1
sums = 0
argo2 = range(argo)
print len(argo2)
for i in argo2:
	sums += num
	num += 5

print sums

sys.exit(0)