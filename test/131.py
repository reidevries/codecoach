'''
Created on 06/01/2013

@author: VIX
'''
import pygame, time

class Sonido(object):
    
    '''
    classdocs
    '''    
    def __init__(self,archivo):
        '''
        Constructor
        ''' 
        self.filename = archivo
        
    
    def reproducir(self):
        pygame.mixer_music.load(self.filename)
        pygame.mixer_music.play()
        
        while pygame.mixer_music.get_busy():
            time.sleep(0.1) 
        
        pygame.mixer_music.stop()