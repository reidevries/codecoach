#! /usr/bin/env python2.6

import re
import sys
import os

InFile = open("Part2.in")
expr = r"(?P<user>[\w.-]+)@(?P<domain>[\w.-]+) +(?P<score>[0-9][0-9]?[.[0-9]+]?)"
argo = "cholly@purdue.edu 90.02"

for line in InFile:
	
	m = re.search(expr, line)
	if m:
		Cato = m.groupdict()
		out = ""
		out += Cato['user']
		out += "@"
		out += "ecn"
		out += Cato['domain']
		out2 = len(out)
		out += ' '
		num = 22-out2
		if out2 < 22:
			num = range(num)
			for I in num:
				out += ' '
		out += Cato['score']
		out += '/100'
		print out
	

sys.exit(0)