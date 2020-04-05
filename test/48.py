def fib(n):
	if n == 0:
		return 0
	if n <= 2: 
		return 1 
	else: 
		print n
		return fib(n - 2) + fib(n - 1)
		
		
print "fib(0) =", fib(0)
print "fib(1) =", fib(1)
print "fib(2) =", fib(2)
print "fib(3) =", fib(3)
print "fib(4) =", fib(4)
print "fib(5) =", fib(5)
print "fib(6) =", fib(6)