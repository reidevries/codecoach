#! /usr/bin/env python2.6

from lists import find_median
import sys

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

sys.exit(0)