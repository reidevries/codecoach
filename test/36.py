import sys

A = []
for I in range(10):
	A.append(I)
print "List A: ", A


A = []
for I in range(10):
	A.insert(0, I)
print "List A: ", A

A = ["A", "Python is cool", [2, 3, 4]]
for I in range(len(A)):
	Item = A.pop(0)
print "Popped item: ", Item
A = ["A", "Python is cool", [2, 3, 4]]
while len(A) > 0:
	Item = A.pop(len(A)-1)
print Item
E = ["B", "T", "A", "H"]
print E
E.sort()
print E

E = [1, 2, 3, 4, 3, 2, 1, 1]
for I in range(5):
	print I+1, "occurs", E.count(I+1), "time(s)"

for I in range(10):
	check = E.count(I+1)
	if check != 0:
		print I+1, " is on the list."
	else:
		print I+1, " is not on the list."
		
		
list1 = [1, 2]
list2 = [3, 4, 5]
list1.extend(list2)
print list1

K =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
del K[4:13]

print max(K)
print sum(K)/len(K)

A = [67, 12, 99, 88, 23]
B = A.sort()
print A, B
print A
print B


S = "Goldfarb:99:mgoldfar@purdue.edu"
T = S.split(":")
U = S.split("@")
V = S.split(":@")
print T
print U
print V

W = S.find("mgoldfar")
print W

X = S.replace("mgoldfar", "thegoldfarb",1)
print X
print S

A = "aaaaaaaaabbbbbbbbbbbbbccccccc"
print A.count("b")

A = A.replace("b", "x", 5)
print A


print int("125")
print complex("125")
print float("125")


for I in range(len(A)):
	num = 0
	num = A[I].count("@purdue.edu")
	if num > 0:
		print A[I]


print range(5)

A ={"Kashi Bakht" : 50, "Sam Tamar" : 70, "Mod Don" : ["foo", "bar"], "Mic Jee" : "Goldfarb" }

print A.keys()
print A.values()
print A["Mic Jee"]
print A.get("Goldfarb")
A["Goldfarb"] = (6, 0)
print A.get("Goldfarb")