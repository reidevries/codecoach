#! /usr/bin/env python2.6

print "Hellow World!"

Name = "Mike"
print "Hello Name\n"

print "Hello", Name, "\n"

print "Hello %s" % (Name,)

X = 200
Y = 300
print X + Y

print "X = %6d, Y = %6d" % (X, Y)

Message = "X = %d, Y = %d" % (X, Y)
print Message

A = [1, 2, 3, 4, 10, 21]

print A[3]

print A[-1]
print A[1:5]

print len(A)

A[2] = "two"
A[4:6] = [4, 5, 6]

print A

print A[1:]

print len(A)

A = A +[len(A)]
print A
A.reverse()

print A
print len(A)

B = A
print A
B.append(10)

print A
print B

B = (1, 2, 3, 4)

print B[0]
print B[3]
print len(B)

print B
#B = B + (9) #creates an error
print B
C = B + (9,)
print C
print B

F = "2.3"

num = 12
num = 12/5
print num
#G = int(F)
#S = print type(F)
