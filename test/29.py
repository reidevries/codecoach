#! /usr/bin/env python2.6
import sys


argv = len(sys.argv)

if argv != 2:
	sys.exit(1)
	
	
argo = sys.argv[1]
argo = int(argo)
sums = 0
while argo > 0:
	sums += argo
	argo -= 1
	
print sums



sys.exit(0)