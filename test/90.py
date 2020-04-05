import string

def extract_author(str):
	if not "," in str:
		arr = str.split()
		if len(arr) > 1 :
			if len(arr) > 2:
				lastname = arr.pop(len(arr) - 1)
				firstname = string.join(arr," ")
				arr = (firstname,lastname)
			(a,b) = arr;
			return (b,a)
		elif len(arr) == 1:
			return (str,"");
	else:
		arr = str.split(",")
		(a,b) = arr;
		b = b.strip();
		return (a,b)
		
		
def extract_authors(str):
	arr = str.split("and")
	authors = []
	for name in arr:
		authors.append(extract_author(name.strip()))
	return authors