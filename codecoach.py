import pyparser
import pyinterpret
import sys

PRINT_OUTPUTS = True				#prints the detected smells, in normal use only this constant will be true
PRINT_STATS = False					#prints the number of smells and the number of unique smells found, for testing the script's succes
PRINT_WHICH_SMELL_STATS = False		#prints which smells were found, also to test the script's success
PRINT_TREE = True					#prints the generated tree, for fun and debugging
PRINT_EXCEPTIONS = False			#prints the exceptions generated by building the tree, turn on to debug it in detail

filename = sys.argv[-1]
if not PRINT_EXCEPTIONS:
	try:
		pyinterpret.tree_build(filename)
	except:
		if (PRINT_STATS): print -1, -1
		elif (not PRINT_STATS) and (not PRINT_WHICH_SMELL_STATS): print "error building the tree"
		exit()
else:
	pyinterpret.tree_build(filename)

if PRINT_TREE: pyinterpret.tree_print()

if PRINT_OUTPUTS: print("Running smell tests...")
stmts_avg = pyinterpret.average_length("statements")
args_avg = pyinterpret.average_length("arguments")

unique = 0
total = 0

fe = 0
lm = 0
ma = 0
fc = 0
mp = 0
rn = 0
nl = 0
mn = 0
nk = 0
uo = 0

l = pyinterpret.sniff_feature_envy()
if (len(l) > 0):
	if PRINT_OUTPUTS:
		print "~~~~Possible feature envy detected at", l
		print "Feature envy describes functions that might be better off in other classes. Usually this is indicated by accessing",
		print "the function from another class more often than on its own. Consider moving the function to a different location in",
		print "the code, if it's convenient and makes sense",
		print "\n"
	unique += 1
	fe += 1
	total += len(l)
	
l = pyinterpret.sniff_long_method(max(4,stmts_avg*2.3))
if (len(l) > 0): 
	if PRINT_OUTPUTS:
		print "~~~~Overly long methods found at", l
		print "A method that is too long indicates that the way you organised your code isn't very reusable or readable.",
		print "This means you may be writing nearly duplicate code in two or more places, which is hard to maintain.",
		print "Or it could just be harder you or other programmers to read in the future. Consider splitting the long method up",
		print "into smaller functions where it feels sensible to do so.",
		print "\n"
	unique += 1
	lm += 1
	total += len(l)
	
l = pyinterpret.sniff_too_many_args(max(4,args_avg*1.5))
if (len(l) > 0): 
	if PRINT_OUTPUTS:
		print "~~~~Functions with too many arguments found at", l
		print "A function with too many arguments is far harder to understand. Consider storing some articles in a data type",
		print "or object, or setting some to '*args' or '**args' to request a variable number of arguments.",
		print "\n"
	unique += 1
	ma += 1
	total += len(l)
	
l = pyinterpret.sniff_functionless_class()
if (len(l) > 0): 
	if PRINT_OUTPUTS:
		print "~~~~Functionless classes found at", l
		print "In most object-oriented programming scenarios, functions are expected to hold data and functions to operate",
		print "on the data. For example, it makes sense that an 'animal' object should not only have a 'vocalisation sound'",
		print "variable, but also be able to use that sound via a function. Consider either adding functions to work on the",
		print "data in this class, or representing the data in one of python's data structures like a named tuple, list or dictionary.",
		print "\n"
	unique += 1
	fc += 1
	total += len(l)

l = pyinterpret.sniff_missing_pair()
if (len(l) > 0): 
	if PRINT_OUTPUTS:
		print "~~~~Expected a pair to be found for functions at", l, ", but none were found"
		print "It'd be intuitive for a pair to exist for this function, (for example, get and set, open and close, etc)",
		print "It's important for code to be intuitive because otherwise future you or other programmers will have a hard time",
		print "understanding the code. Consider adding the appropriate pair function.",
		print "\n"
	unique += 1
	mp += 1
	total += len(l)

l = pyinterpret.sniff_redundant_name()
if (len(l) > 0):
	if PRINT_OUTPUTS: 
		print "~~~~Functions with redundant names found at", l
		print "It's unnecessary for your function name to be this long. Clean it up by removing anything redundant.",
		print "\n"
	unique += 1
	rn += 1
	total += len(l)

l = pyinterpret.sniff_nested_loops()
if (len(l) > 0):
	if PRINT_OUTPUTS:
		print "~~~~Nested for loops found at", l
		print "There are a lot of for loops inside one another here! You probably could have solved the problem in a simpler way:",
		print "it is rare for experienced programmers to use this many for loops inside one another. Consider rewriting the method",
		print "using recursion, or thinking in depth about the problem to see if there is an easier way to solve it.",
		print "\n"
	unique += 1
	nl += 1
	total += len(l)
	
l = pyinterpret.sniff_magic_number()
if (len(l) > 0):
	if PRINT_OUTPUTS:
		print "~~~~\"Magic Numbers\" found at",
		for item in l:
			print item, ",",
		print "Is this number chosen by trial and error? In most cases, it's better to choose a number based on exact calculations",
		print " and store it in a variable. For example, use a label named 'GRAVITY' set to 9.81 instead of writing it in manually",
		print " or make a variable called 'character speed' instead of relying on a fixed number. This will allow you to make changes",
		print " more easily later on.",
		print "\n"
	unique += 1
	mn += 1
	total += len(l)
	
l = pyinterpret.sniff_no_keywords()
if (len(l) > 0):
	if PRINT_OUTPUTS:
		print "~~~~Function calls without keywords found at",
		for item in l:
			print item, ",",
		print "If a call is made to a function that takes more than three or so arguments, it's better to include keyword arguments",
		print ".For example write make_sound(animal=\"bear\", age=15, size=2, distance=94) instead of the more confusing make_sound(\"bear\",15,2,94)",
		print "\n"
	unique += 1
	nk += 1
	total += len(l)

l = pyinterpret.sniff_unsafe_open()
if (len(l) > 0):
	if PRINT_OUTPUTS:
		print "~~~~Unsafe file open found at",
		for item in l:
			print item, ",",
		print "If opening a file, it's safer to use 'with' and 'as' keywords. This is because the file will always be closed properly,",
		print "and all errors will be safely caught. Use 'with open(f) as file' rather than 'file = open(f)'",
		print "\n"
	unique += 1
	uo += 1
	total += len(l)
	
if PRINT_OUTPUTS: 
	print "Done," 
	if PRINT_STATS: print "unique smells: total smells:"
if PRINT_STATS: print unique,total
if PRINT_WHICH_SMELL_STATS: print fe, lm, ma, fc, mp, rn, nl, mn, nk, uo
