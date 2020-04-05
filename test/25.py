import sys
import random

line_movies = list()
line_names = list()
numbers = list()
story = list()

for line in open('newone.txt'):
  line = line.strip()
  line_movies.append(line)
   
random.shuffle(line_movies)

for nline in open('newone1.txt'):
  nline = nline.strip()
  line_names.append(nline)

for number in open('numbers.txt'):
  number = number.strip()
  numbers.append(number)

  
for stor in open('story.txt'):
  stor = stor.strip()
  story.append(stor)

random.shuffle(story)

for i in range(0,9):
  print "In " +numbers[i]+ ", You watch " + line_movies[i].lower()+ " with " + line_names[i]+ "\n" + story[i]+"\n"