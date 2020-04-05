import sys
import os

argv = len(sys.argv)

if argv != 2:
	print "Usage: ./attributes.py"
	sys.exit(1)
	
file = sys.argv[1]
	
if os.path.exists(file):
	print file, "exists"
else:
	print file, "does not exist"
	sys.exit(0)

if os.path.isdir(file):
	print file, "is a directory"
else:
	print file, "is not a directory"
	
if os.path.isfile(file):
	print file, "is an ordinary file"
else:
	print file, "is not an ordinary file"
	
	
if os.access(file, os.R_OK):
	print file, "is readable"
else:
	print file, "is not readable"
	
	
if os.access(file, os.W_OK):
	print file, "is writable"
else:
	print file, "is not writable"
	
	
if os.access(file, os.X_OK):
	print file, "is executable"
else:
	print file, "is not executable"
	
sys.exit(0)