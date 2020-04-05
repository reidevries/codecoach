#!/usr/bin/python
"""
main.py
Pomodoro Simple - a timer in python
Google Pomodoro for more information.

@author Hamish Macpherson
@url http://hami.sh/
"""

import time
import sys, os
import pygame.mixer

# Constants
DEFAULT_TIME = 25
CURRENT_PATH = os.path.dirname(sys.argv[0])
DING_FILE = os.path.join(CURRENT_PATH, 'ding.ogg')

# Setup Ding
pygame.mixer.init()
DING = pygame.mixer.Sound(DING_FILE)
DING.set_volume(.5)

# Functions
def ding():    
    DING.play()

def start(minutes):  
    try:
        print "Starting Pomodoro for %s minutes..." % minutes
        print "Press [Ctrl + C] to quit."

        os.system('growlnotify -m "Pomodoro" -t "%s minute timer started"' % minutes)

        minutes = int(minutes)
        timer_width = minutes * 3
        sys.stdout.write("[%s]" % (" " * timer_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (timer_width+1))

        for i in xrange(minutes * 3):
            time.sleep(60/3)
            sys.stdout.write("=")
            sys.stdout.flush()

        ding()
        os.system('growlnotify -m "Pomodoro" -t "%s minute timer completed"' % minutes)    
        sys.stdout.write("\n")       
    
    except KeyboardInterrupt:
        os.system('clear')
        sys.exit()

if __name__ == '__main__':
    ding()
    try:
        minutes = sys.argv[1]
        start(minutes)
    except IndexError:
        start(DEFAULT_TIME)