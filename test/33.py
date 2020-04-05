import sys
import os

argv = len(sys.argv)

if argv != 3:
	print "Usage: statify.py"
	sys.exit(1)

argo = sys.argv[1]

if (os.path.exists(argo) == 0):
	print argo, "does not exist!"
	sys.exit(1)
	
	
output = sys.argv[2]


if os.path.exists(output):
	print output, "already exists!"
	sys.exit(1)
	
InFile = open(argo, "r")
OutFile = open(output, "w")
LineNum = 1
WordCount = 0
LetterNum = 0
for line in InFile:
	OutFile.write("%4d" % (LineNum))
	OutFile.write(": ")
	OutFile.write(line)
	LineNum = LineNum + 1
	SpaceSplit = line.split(" ")
	WordCount += len(SpaceSplit)
	LetterNum = LetterNum + len(line) - len(SpaceSplit)
	
AverageWord = float(LetterNum)/float(WordCount)
OutFile.write("---- Document statistics ----\n")
OutFile.write("Line count: %d\n" % (LineNum))
OutFile.write("Word count: %d\n" % (WordCount))
OutFile.write("Average word size: %.3f\n" % AverageWord)





sys.exit(0)