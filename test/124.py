'''
Created on 06/01/2013

@author: 
    Victor Rodriguez 
    Jimmy Banchon
'''
# Importacion de librerias
import pygame
import Sonido
import random, os, sys

#Declaracion de funciones
def eleccion(name):
    n = True

    pygame.mixer.music.load(name)
    pygame.mixer.music.play(-1)
    while n:
        n_puerta = 0
        n_puerta= input('''
                        [1] Puerta 1
                        [2] Puerta 2
                        Escoja 1 sola puerta: ''')
           
        if (2 >= n_puerta > 0):
            n = False
            pygame.mixer.music.stop()
    
    return n_puerta

def eleccion_dragon(name):
    n = True

    while n:
        n_puerta = 0
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(-1)
        n_puerta= input('''
                        [1] Combatir contra el Dragon
                        [2] Intentar huir
                        Escoja 1 sola puerta: ''')
           
        if (2 >= n_puerta > 0):
            n = False
            pygame.mixer.music.stop()
    
    return n_puerta

# Declaracion del main

if __name__ == "__main__":

    pygame.mixer.init()
    
    numero = 0

    intro = Sonido.Sonido("Sounds/intro.wav")
    
    decision = Sonido.Sonido("Sounds/2puertas_mixdown.wav")
    puerta = Sonido.Sonido("Sounds/puerta.wav")
    #Ramal 1
    guardian = Sonido.Sonido("Sounds/pelea_con_guardianes.wav")
    escaleras = Sonido.Sonido("Sounds/escaleras.wav")
    #decision
    narracion = Sonido.Sonido("Sounds/narracion.wav")
    trampa = Sonido.Sonido("Sounds/trampa_mixdown_nuevo.wav")
    
    #Opcion 2
    dragon = Sonido.Sonido("Sounds/pelea_dragon_mixdown.wav")
    pelea_dragon_ganada = Sonido.Sonido("Sounds/pelea_dragon_gana_mixdown.wav")
    pelea_dragon_muere = Sonido.Sonido("Sounds/pelea_dragon_muere_mixdown.wav")
    caballero_deborado = Sonido.Sonido("Sounds/pelea_dragon_muere_mixdown.wav")
    princesa = Sonido.Sonido("Sounds/final_despues_dragon_mixdown.wav")
    
    #Ramal 2
    normal = Sonido.Sonido("Sounds/Normal_1_mixdown.wav")
    #escaleras
    #decision
    
    #Opcion 1
    troll = Sonido.Sonido("Sounds/pelea_troll_mixdown.wav")
    juego = Sonido.Sonido("Sounds/eleccion_juego_mixdown.wav")
    caballero_pierde_juego = Sonido.Sonido("Sounds/eleccion_juego_muerto_mixdown.wav")

    caballero_gana_juego = Sonido.Sonido("Sounds/") 
    
    pelea_mago = Sonido.Sonido("Sounds/pelea_mago_mixdown.wav")
    pelea_mago_gana = Sonido.Sonido("Sounds/pelea_mago_gana_mixdown.wav") 
    pelea_mago_pierde = Sonido.Sonido("Sounds/pelea_mago_muere_mixdown.wav")
    
    
    #Implementacion -------------------------------------------------------
    intro.reproducir()
    
    os.system("cls")
    decision.reproducir()
    print('Escoja el numero de puerta que sea dirigirse:')
    numero = eleccion("Sounds/sonido_espera.wav")
    puerta.reproducir() 
    
    if numero==1:
        guardian.reproducir()
        escaleras.reproducir()
        
        os.system("cls")
        decision.reproducir()
        print('Escoja el numero de puerta que sea dirigirse:')
        numero = eleccion("Sounds/sonido_espera.wav")
        puerta.reproducir() 
        
        if(numero==1):
            narracion.reproducir()
            trampa.reproducir()
            sys.exit()
        else:
            dragon.reproducir()
            
            os.system("cls")
            decision.reproducir()
            print('Escoja que accion desea hacer:')
            numero = eleccion_dragon("Sounds/sonido_espera.wav")
            puerta.reproducir() 
            
            if(numero == 1):
                aleat = int(random.random())
                
                if(aleat == 1):
                    pelea_dragon_ganada.reproducir()
                    princesa.reproducir()
                else:
                    pelea_dragon_muere.reproducir()
            else:
                caballero_deborado.reproducir()
            sys.exit()        
    else:
        normal.reproducir()
        escaleras.reproducir()
        
        os.system("cls")
        decision.reproducir()
        print('Escoja el numero de puerta que sea dirigirse:')
        numero = eleccion("Sounds/sonido_espera.wav")
        puerta.reproducir() 
            
        if(numero == 1):
            troll.reproducir()
            juego.reproducir()
            
            aleat = 1 + int(random.random()*5)
            numero = input('Escriba el numero que usted cree que tiene Zagal: ')  
            
            if(aleat == numero):
                caballero_gana_juego.reproducir()
                dragon.reproducir()
            
                os.system("cls")
                decision.reproducir()
                print('Escoja que accion desea hacer:')
                numero = eleccion_dragon("Sounds/sonido_espera.wav")
                puerta.reproducir() 
                
                if(numero == 1):
                    aleat = int(random.random())
                    
                    if(aleat == 1):
                        pelea_dragon_ganada.reproducir()
                        princesa.reproducir()
                    else:
                        pelea_dragon_muere.reproducir()
                else:
                    caballero_deborado.reproducir()
                sys.exit()
            else:
                caballero_pierde_juego.reproducir()
        
        else:
            pelea_mago.reproducir()
            
            numero = input('''
                Escoja que accion tomara contra el mago Zagal:
                [1] Rebotarle el hechizo con la espada
                [2] Cubrirse de los hechizos
                ''')
            
            if(numero == 1):
                pelea_mago_gana.reproducir()
                princesa.reproducir()
            else:
                pelea_mago_pierde.reproducir()
                
            sys.exit()   