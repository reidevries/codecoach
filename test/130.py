'''
Created on 10/01/2013

@author: VIX
'''

import pygame

class Repr(pygame.mixer.Sound, object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = "Sounds/"+name+".wav"