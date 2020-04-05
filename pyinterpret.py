import pprint
import pyparser
import re

tree = {}

INTERPRETER_DEBUG = False

def tree_build(filename):
	global tree
	tree = pyparser.parse_file(filename)
	
def tree_print():
	"""prints the tree in a pretty way"""
	global tree
	print("class\t\tfunc\t\tcontents")
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(tree)

def average_length(lengthkey):
	'''finds average length of either a method or arguments list for statistics purposes'''
	totallength = 0
	totalcount = 0
	for classkey in tree:
		for funckey in tree[classkey]:
			if (lengthkey == "arguments"):
				thislength = count_args(tree[classkey][funckey])
			elif (lengthkey == "statements"):
				thislength = count_stmts(tree[classkey][funckey])

			if (thislength > 0):
				totallength += thislength
				totalcount += 1
				if (INTERPRETER_DEBUG): print "number of", lengthkey, "for class", classkey, "func", funckey, "was", thislength

	if (totalcount > 0):
		return totallength/totalcount
	else:
		return 0
	
def count_stmts(branch):
	'''counts the number of statements in a function (or other, but usually used for functions)'''
	stmtno = 0
	if (type(branch) == dict):
		if "statements" in branch:
			stmtno = len(branch["statements"])			#get the number of statements in the main function
		for key in branch:									#get the number of statements in child fields (for loops, if clauses etc)
			if (type(branch[key]) == dict):
				stmtno += count_stmts(branch[key])
				stmtno += 1									#the child statement itself is a statement

	return stmtno														
	
def count_args(branch):
	'''counts the number of arguments in a function or class'''
	if (type(branch) == dict):
		if "arguments" in branch:
			return len(branch["arguments"])
	return 0

def count_functions(classkey):
	'''counts the number of functions in a class'''
	if (type(tree[classkey]) == dict):
		nummethods = 0
		if "arguments" in tree[classkey]:	#subtract non-method entries from the output length
			nummethods -= 1
		if "statements" in tree[classkey]:	#same
			nummethods -= 1
		if "base" in tree[classkey]:		#same
			nummethods -= 1
		nummethods += len(tree[classkey])
		if (INTERPRETER_DEBUG): print("{} methods found in class {}").format(nummethods,classkey)
		return nummethods
	else:
		return 0														#if it isn't a real class obviously it contains 0 functions

def list_of_stmts(branch, appendlist):
	'''returns a list of all statements including nested statements'''
	if (type(branch) == dict):
		if (len(branch) > 2):											#if the branch contains more than just arguments&statements
			for key in branch:
				if (key != "statements" and key != "arguments"):
					appendlist += list_of_stmts(branch[key], appendlist)
		if "statements" in branch:
			return appendlist + branch["statements"]
	return appendlist

def search_branch(t, term, path=None):									#searches for keywords at the end of branches (or join points of branches)
	if path is None:
		path = []
	
	if isinstance(t, list) or isinstance(t, tuple):
		for i in t:
			new_path = list(path)
			
			if isinstance(i, tuple) and isinstance(t, list):			#if it's a tuple inside a list, append it
				new_path.append(i)
			
			for result in search_branch(i, term, path=new_path):		#look down the path further	
				yield result
	elif isinstance(t, dict):
		for key,val in t.items():
			new_path = list(path)
			new_path.append(key)
			
			if isinstance(val, tuple):									#if it's a tuple inside a dict, append it
				new_path.append(val)
			
			for result in search_branch(val, term, path=new_path):		#look down the path further	
				yield result
	elif re.match(term, str(t), re.X):									#if the end of the tree is reached, yield it
		yield list(path)

def search_keys(t, term, path=None):									#searches for keywords in dictionary keys
	if path is None:
		path = []

	if (isinstance(t, dict)):											#if it's a dictionary
		for key, val in t.items():										#get every key and val in the dict
			if (isinstance(val, dict)):									#only continue if the value is a dictionary
				new_path = list(path)
							
				nodictchildren = True									#if it has dicts as children,
				for k in val:											# we should keep traversing the tree until we find the end
					if isinstance(val[k], dict):
						nodictchildren = False

				if nodictchildren:										#if we can't traverse the tree anymore,
					for i in range(1, len(new_path)+1):					#loop through the path in reverse, 
						if re.match(term, str(new_path[-i]), re.X):		# check for matches
							yield new_path[:len(new_path)+1-i]			# at the deepest match, return the path up to that match
							break
				else:													#no need to continue unless there are dict children
					new_path.append(key)
					for result in search_keys(val, term, new_path):
						yield result

def sniff_functionless_class():
	'''finds classes that have no functions'''
	nameslist = []
	for classkey in tree:
		if (classkey != "base"):										#if the class is the base class, it doesn't matter if it has no functions
			if (count_functions(classkey) == 0):
				nameslist.append(classkey)								#if there are no functions, add the class name to the list
	return nameslist

def sniff_redundant_name():
	'''finds functions containing the parent class\'s name'''
	nameslist = []
	for classkey in tree:
		if (classkey != "base"):
			for funckey in tree[classkey]:
				if classkey in funckey:									#if the function name contains the class name, a redundant name was found
					nameslist.append((classkey, funckey))
	return nameslist
	#Note: this could be improved by including function names which share a common infix for a large number of functions

def sniff_long_method(thresh=10):
	'''searches for methods that are too long'''
	nameslist = []
	for classkey in tree:
		for funckey in tree[classkey]:
			if (count_stmts(tree[classkey][funckey]) > thresh):
				nameslist.append((classkey, funckey))
	return nameslist

def sniff_too_many_args(thresh=10):
	'''searches for methods with too many arguments'''
	nameslist = []
	for classkey in tree:
		for funckey in tree[classkey]:
			if (count_args(tree[classkey][funckey]) > thresh):
				nameslist.append((classkey, funckey))
	return nameslist
	
def sniff_feature_envy():
	'''searches for functions that would make more sense in another class'''
	returnlist = []
	for c in tree:
		for funcname in tree[c]:
			if (funcname != "base"):
				functionnums = {}
				for i in search_branch(tree, funcname):					#first, count occurrences of calls to the function
					term = funcname
					if (str(i[-1][0]) == '.'):							#if it's a call from other classes or w/e
						term = str(i[-1][1]) + '.' + term

					if term in functionnums:
						functionnums[term] += 1
					else:
						functionnums[term] = 1
				
				for key in functionnums:								#if any calls are more common than direct calls,
					if (funcname in functionnums and 
						functionnums[key] > functionnums[funcname]):	# feature envy might exist
						if not funcname in returnlist:
							returnlist.append(funcname)
	return returnlist

def sniff_missing_pair():
	'''searches for functions that should have a corresponding pair, like get() and set()'''
	NAME_PAIRS = [	("get",	"set"),									#list of pairs of names
					("open", "close"),								#this allows new names to be added easily
					("start", "stop")]
	
	nameslist = []	#list of lists of tuples, the tuples are of the format (name, list of functions in which name appears)
					#read as nameslist[pair index][index of a or b in the pair][index of function in which name appears + 1]
	
	for pair in NAME_PAIRS:
		alist = []
		blist = []
		for classkey in tree:
			for funckey in tree[classkey]:							#look for members of the pair
				if pair[0] in funckey:
					funcwoutname = funckey.replace(pair[0], "")		#save in list without the NAME_PAIRS name
					alist.append(funcwoutname)
				elif pair[1] in funckey:
					funcwoutname = funckey.replace(pair[1], "")		#save in list without the NAME_PAIRS name
					blist.append(funcwoutname)
		nameslist.append([
							(pair[0],alist), 
							(pair[1],blist)
						])
	if (INTERPRETER_DEBUG): print "found paired functions of types ", nameslist
	
	funclist = []		#list of the functions that have no match
	for name in nameslist:
		aname = name[0][0]	#get
		bname = name[1][0]	#set
		alist = name[0][1]	#list of funcs containing "get" without the "get" part
		blist = name[1][1]	#list of funcs containing "set"	without the "set" part
		for afunc in alist:
			if afunc not in blist:
				funclist.append(aname+afunc)
		for bfunc in blist:
			if (bfunc not in alist and bfunc not in funclist):
				funclist.append(bname+bfunc)
	return funclist

def sniff_code_in_comments():
	"""searches for python syntax in comments, like brackets and colons"""
	#unimplementable as long as comments are ignored
	
def sniff_nested_loops():
	"""finds heavily nested loops (or if checks) which may have more efficient solutions"""
	MAGIC_NUMBER = 3
	nestedforslocations = []
	for item in search_keys(tree, r"for"):
		if (len(item) > MAGIC_NUMBER):
			nestedforslocations.append(item)
	return nestedforslocations

def sniff_unsafe_open():
	"""searches for files or scripts imported/opened without with or as tags"""
	returnlist = []
	for item in search_branch(tree, "open"):
		returnlist.append(item)
	return returnlist

def sniff_unused_code():
	"""checks each function/class to see if its referenced elsewhere"""

def sniff_no_keywords():
	"""checks lists of arguments in method references longer than MAGIC_NUMBER to see if they have keyword descriptors
		eg bob(True, 20, \"henlo\") is more confusing than bob(dothis=True, count=20, hi=\"henlo\")"""
	returnlist = []
	for c in tree:
		for f in tree[c]:
			if 'statements' in tree[c][f]:
				for stmt in tree[c][f]['statements']:
					if (len(stmt) == 2 and type(stmt[1]) == list and len(stmt[1]) > 3):
						returnlist.append(stmt)
	return returnlist

def sniff_magic_number():
	"""finds numbers which seem to have no objective basis and are not defined as constants at the beginning of the code
		eg speed = 6.37*direction"""
	returnlist = []
	for item in search_branch(tree, r"(\d+\.\d*|\.\d+)([eE][-+]? \d+)?"):
		c = ""
		f = ""
		if (len(item) >= 3):
			c = str(item[0])
			f = str(item[1])
			result = str(item[-1]) + " found at class "+c+" func "+f
		if (f != ""):
			returnlist.append(result)	#the search returns the entire path to the element, but we only want the last bit; the element itself
	return returnlist
