#! /usr/bin/env python2.6

import sys
import os

def find_median(list1, list2):
	list1.extend(list2)
	length = len(list1)
	medianPOS = length/2
	median = list1[medianPOS]
	#final = tuple(total)
	final = (median, list1)
	return final
	

if __name__ == "__main__":
	print "Enter the first list of numbers: ",
	data1 = sys.stdin.readline()
	print "Enter the second list of numbers: ",
	data2 = sys.stdin.readline()
	data1 = data1.split()
	data1 = map(int, data1)
	data2 = data2.split()
	data2 = map(int, data2)
	(Median, Sorted_List) = find_median(data1, data2)
	print "First list:",data1
	print "Second list:",data2
	print "Merged list:",Sorted_List
	print "Median:",Median

