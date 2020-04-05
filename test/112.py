# -*- coding: utf-8 -*-
'''
Created on Jun 27, 2012

@author: SebaGames
'''

if __name__ == '__main__':
    pass

import pygame
import game
import nozar_game
        
pygame.init();

xoConfig = False;
fastKey = False;

if xoConfig:
    scale = 4;
    updateCount = 1;
    useFilter = not True;
else:
    scale = 2;
    updateCount = 1;
    useFilter = False;
    
mute = not True;
    
screen = pygame.display.set_mode([300 * scale,225 * scale]);
pygame.display.set_caption("LA TORRE DE NOZAR (SEBAGAMES)");
    

#screen = pygame.display.set_mode([300 * scale,225 * scale]);

clock = pygame.time.Clock();

done = False;

fps = 60/updateCount;

g = game.Game();
#gs = nozar_game.GameplayState();
gs = nozar_game.TitleState();
#gs = nozar_game.EndingState();
g.init(gs, screen, scale, useFilter, mute);
nozar_game.GameCommands.startGame(g);

while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True; # Flag that we are done so we exit this loop
 
    i = updateCount;
    while i > 0 and not done:
        keys = pygame.key.get_pressed();
        nozar_game.GameCommands.updateKeys(keys);
        
        if keys[pygame.K_LALT] and keys[pygame.K_F4]:
            done = True;
            
        g.update();
        
        if fastKey and keys[pygame.K_r]:
            g.update();
            g.update();
            g.update();
            g.update();
        
        i -= 1;
    

    g.render();
    
    # Limit to fps value
    clock.tick(fps);
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip();

g.destroy();
pygame.quit();