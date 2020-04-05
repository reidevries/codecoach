import os, re
n = 1
for i in os.listdir('.'):
	os.rename(i, re.sub(r'.+', '{}.py'.format(n), i))
	n += 1
	print(n)    
