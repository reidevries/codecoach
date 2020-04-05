import sys
import os

def fact_iter(n):
	number = 0
	for I in range(n+1):
		number = number * I
		if I == 0:
			number = 1
		final = number
	return final
		
def fact(n):
	number = 1
	if n != 0:
		number =n*fact(n-1)
	final = number
	return number
		
def fib_iter(n):
	number1 = 0
	number2 = 0
	temp = 0
	for I in range(n+1):
		final = number2
		temp = number2
		number2 = number2 + number1
		number1 = temp
		if number2 == 0:
			number2 = 1
	return final		

def fib(n):
	if n == 0:
		return 0
	if n <= 2: 
		return 1 
	else: 
		return fib(n - 2) + fib(n - 1)
	
def stats(enter):
	length=len(enter)
	count = length
	length = range(length)
	average = 0
	minimum= -1
	maximum = 0
	summation = 0
	for I in length:
		summation = summation+enter[I]
		if enter[I] > maximum:
			maximum = enter[I]
			
		if enter[I] < minimum:
			minimum = enter[I]
		if minimum == (-1):
			minimum = enter[I]
	average = float(summation)/count
	final = (minimum, maximum, summation, count, average)
	return final
	


print "fact_iter(0) =", fact_iter(0)
print "fact_iter(1) =", fact_iter(1)
print "fact_iter(2) =", fact_iter(2)
print "fact_iter(3) =", fact_iter(3)
print "fact_iter(4) =", fact_iter(4)
print "fact_iter(5) =", fact_iter(5)
print""
print "fact(0) =", fact(0)
print "fact(1) =", fact(1)
print "fact(2) =", fact(2)
print "fact(3) =", fact(3)
print "fact(4) =", fact(4)
print "fact(5) =", fact(5)
print""
print "fib_iter(0) =", fib_iter(0)
print "fib_iter(1) =", fib_iter(1)
print "fib_iter(2) =", fib_iter(2)
print "fib_iter(3) =", fib_iter(3)
print "fib_iter(4) =", fib_iter(4)
print "fib_iter(5) =", fib_iter(5)
print "fib_iter(6) =", fib_iter(6)
print""
print "fib(0) =", fib(0)
print "fib(1) =", fib(1)
print "fib(2) =", fib(2)
print "fib(3) =", fib(3)
print "fib(4) =", fib(4)
print "fib(5) =", fib(5)
print "fib(6) =", fib(6)

print "stats([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) =", stats([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
