# -*- coding: utf-8 -*-
from __future__ import division;
import pygame;
from random import choice;
import random;
import math;
import game;

import levels;

def sign(x):
    if x < 0:
        return -1;
    elif x > 0:
        return 1;
    else:
        return 0;

class Anim:
    def __init__(self, aLoopIndex, aFrameDuration, aFrames):
        self.frames = aFrames;
        self.frameDuration = aFrameDuration;
        self.loopIndex = aLoopIndex;

class GameControl:
    def __init__(self):
        self.a = False;
        self.b = False;
        self.c = False;
        self.left = False;
        self.right = False;
        self.up = False;
        self.down = False;
        self.anyDir = False;
        self.anyH = False;
        self.anyV = False;
        self.anyButton = False;
        
    def updateWithKeys(self, aKeys, aKeyForA, aKeyForB, aKeyForC, aKeyU, aKeyD, aKeyL, aKeyR):
        
        self.anyDir = False;
        self.anyH = False;
        self.anyV = False;
        self.anyButton = False;
        
        if not self.a and aKeys[aKeyForA]:
            self.a = True;
            self.anyButton = True;
        else:
            self.a = False;
            
        if not self.b and aKeys[aKeyForB]:
            self.b = True;
            self.anyButton = True;
        else:
            self.b = False;
            
        if not self.c and aKeys[aKeyForC]:
            self.c = True;
            self.anyButton = True;
        else:
            self.c = False;
            
        if aKeys[aKeyU]:
            self.up = True;
            self.anyDir = True;
            self.anyV = True;
        else:
            self.up = False;
            
        if aKeys[aKeyD]:
            self.down = True;
            self.anyDir = True;
            self.anyV = True;
        else:
            self.down = False;
            
        if aKeys[aKeyL]:
            self.left = True;
            self.anyDir = True;
            self.anyH = True;
        else:
            self.left = False;
            
        if aKeys[aKeyR]:
            self.right = True;
            self.anyDir = True;
            self.anyH = True;
        else:
            self.right = False;
        
    def forward(self, aDirection):
        if (self.left and aDirection == -1) or (self.right and aDirection == 1):
            return True;
        else:
            return False;
        
    def back(self, aDirection):
        if (self.left and aDirection == 1) or (self.right and aDirection == -1):
            return True;
        else:
            return False;

GAME = None;

GAME_LIMIT_LEFT = 20;
GAME_LIMIT_RIGHT = 300 - GAME_LIMIT_LEFT;
GAME_LIMIT_BACK = 0;
GAME_LIMIT_FRONT = 140;

#Gameplay constants
GAME_MIN_ENEMIES = 1;
GAME_MAX_ENEMIES = 5;
GAME_MIN_DIAMONDS_PER_ENEMY = 1;
GAME_MAX_DIAMONDS_PER_ENEMY = 5;

GAME_LEVEL_AMOUNT = 12;

GAME_ENEMY_MIN_LIFE = 1;
GAME_ENEMY_MAX_LIFE = 50;



WALL_POS = 135;

global IMGLIB_CHARACTER;
global IMGLIB_ATTACKS;
global IMGLIB_GHOST;
global IMGLIB_GHOST_NEGATIVE;
global IMGLIB_EFFECTS;
global IMGLIB_NUMBER_ONE;
global IMGLIB_NUMBER_ONE_NEGATIVE;
global IMGLIB_MISC;
IMGLIB_CHARACTER = None;
IMGLIB_ATTACKS = None;
IMGLIB_GHOST = None;
IMGLIB_GHOST_NEGATIVE = None;
IMGLIB_EFFECTS = None;
IMGLIB_NUMBER_ONE = None;
IMGLIB_NUMBER_ONE_NEGATIVE = None;
IMGLIB_MISC = None;

ANIM_CHARACTER_STAND = Anim(0, 3, ("stand00","stand01","stand02","stand03","stand04","stand05","stand05","stand06","stand06"));
ANIM_CHARACTER_WALK = Anim(0, 4, ("walk00", "walk01", "walk02", "walk03", "walk04", "walk05", "walk06", "walk07"));
ANIM_CHARACTER_ATTACK_A = Anim(-1, 3, ("attack_a00", "attack_a01", "attack_a01", "attack_a02", "attack_a03", "attack_a03", "attack_a04", "attack_a04", "attack_a05", "attack_a06", "attack_a07", "attack_a08"));
ANIM_CHARACTER_WIN = Anim(-1, 3, ("attack_a00", "attack_a01", "attack_a01", "attack_a02", "attack_a03", "attack_a03", "attack_a04", "attack_a04", "attack_a05", "attack_a06", "attack_a07", "attack_a08","attack_a01", "attack_a00", "attack_a01", "attack_a00"));

ANIM_GHOST_APPEARING = Anim(-1, 3, ("appear00", "appear01", "appear02", "appear03", "appear04", "appear05", "appear06", "appear07", "normal00"));
ANIM_GHOST_NORMAL = Anim(0, 3, ("normal00", "normal00", "normal00", "normal00", "normal00", "normal00", "normal00", "normal00", "normal01", "normal00"));
ANIM_GHOST_LAUGH = Anim(1, 12, ("appear07", "laugh00", "laugh01"));
ANIM_GHOST_DAMAGE = Anim(0, 2, ("damage01", "damage00"));
ANIM_GHOST_DEAD = Anim(-1, 4, ("damage00", "damage01", "damage00", "damage01", "appear05", "appear04", "appear03", "appear02", "appear01", "appear00"));

ANIM_DIAMOND = Anim(0, 4, ("diamond00", "diamond01", "diamond02", "diamond03", "diamond04", "diamond05", "diamond06", "diamond07", "diamond08", "diamond09", "diamond10", "diamond11", "diamond10", "diamond12", "diamond00", "diamond00", "diamond00", "diamond00"));
ANIM_SPARK = Anim(-1, 1, ("simple_spark", "flare", "simple_spark", "flare", "simple_spark", "flare"));
ANIM_EFF_SIMPLE_SPARK = Anim(-1,2, ("simple_spark", "simple_spark"));
ANIM_HUD_DIAMOND = Anim(0, 4, ("hud_diamond00", "hud_diamond01", "hud_diamond02", "hud_diamond03", "hud_diamond04", "hud_diamond00", "hud_diamond04", "hud_diamond04", "hud_diamond00", "hud_diamond04", "hud_diamond00", "hud_diamond00", "hud_diamond00", "hud_diamond00", "hud_diamond00"));

ANIM_NUMBER_ONE_APPEARING = Anim(-1, 2, ("spawn00", "spawn01", "spawn02", "spawn03", "spawn04", "spawn05"));
ANIM_NUMBER_ONE_IDLE_A = Anim(0, 12, ("stand00", "stand01"));
ANIM_NUMBER_ONE_IDLE_B = Anim(0, 4, ("stand02", "stand02", "stand00", "stand03", "stand03", "stand00"));
ANIM_NUMBER_ONE_DEADING = Anim(-1, 2, ("spawn05", "spawn04", "spawn03", "spawn02", "spawn01", "spawn00"));
ANIM_NUMBER_ONE_WALKING = Anim(0, 4, ("run00", "stand01", "run01", "stand00"));
ANIM_NUMBER_ONE_STEALING = Anim(-1, 6, ("take00", "stand02", "stand01", "happy00", "happy01", "happy00", "happy01", "happy00", "stand00", "stand00"));
ANIM_NUMBER_ONE_DAMAGE = Anim(2, 2, ("spawn02", "spawn05", "stand00", "spawn04"));

global SND_GHOST_DAMAGE;
global SND_GHOST_LAUGH;
global SND_GHOST_DEAD;
global SND_ATTACK_LAUNCH;
global SND_NUMBER_ONE_DAMAGE;
global SND_DIAMOND_BOUNCE;
global SND_DIAMOND_GET;
global SND_CLOCK_PAIR;
global SND_CLOCK_UNPAIR;
global SND_NOZAR_APPEAR;
SND_GHOST_DAMAGE = None;
SND_GHOST_LAUGH = None;
SND_GHOST_DEAD = None;
SND_ATTACK_LAUNCH = None;
SND_NUMBER_ONE_DAMAGE = None;
SND_DIAMOND_BOUNCE = None;
SND_DIAMOND_GET = None;
SND_CLOCK_PAIR = None;
SND_CLOCK_UNPAIR = None;
SND_NOZAR_APPEAR = None;


CTRL1 = GameControl();

GAME_PAIR_VALUES = (2,4,6,8);
GAME_NOT_PAIR_VALUES = (1,3,5,7,9);

global KEY_STATE_PREV;
global KEY_STATE;
KEY_STATE_PREV = None;
KEY_STATE = None;

global FNT_CLEARLY;
global FNT_CLEARLY_DARK;
global FNT_TIME;
FNT_CLEARLY = None;
FNT_CLEARLY_DARK = None;
FNT_TIME = None;

class GameCommands:
    @staticmethod
    def startGame(aGame):
        #print "to do: load all resources here";
        
        global FNT_CLEARLY;
        FNT_CLEARLY = aGame.loadFont("assets/graphics/fonts/clearly.png", (10,12), (-2,0), "0123456789+-%:=,.ABCDEFGHIJKLMNnOPQRSTUVWXYZaeiou!^?&`';y()<>zxc/");
        
        global FNT_CLEARLY_DARK;
        FNT_CLEARLY_DARK = aGame.loadFont("assets/graphics/fonts/clearly_dark.png", (10,12), (-2,0), "0123456789+-%:=,.ABCDEFGHIJKLMNnOPQRSTUVWXYZaeiou!^?&`';y()<>");
        
        global FNT_TIME;
        FNT_TIME = aGame.loadFont("assets/graphics/fonts/numeric.png", (8,9), (0,0),"0123456789");
        
        
        global IMGLIB_CHARACTER;
        global IMGLIB_ATTACKS;
        global IMGLIB_GHOST;
        global IMGLIB_GHOST_NEGATIVE;
        global IMGLIB_EFFECTS;
        global IMGLIB_NUMBER_ONE;
        global IMGLIB_NUMBER_ONE_NEGATIVE;
        global IMGLIB_MISC;
        
        IMGLIB_CHARACTER = aGame.loadImageLib("assets/graphics/libs/character/character.xml");
        IMGLIB_ATTACKS = aGame.loadImageLib("assets/graphics/libs/attacks/attacks.xml");
        IMGLIB_GHOST = aGame.loadImageLib("assets/graphics/libs/ghost/ghost.xml");
        IMGLIB_GHOST_NEGATIVE = aGame.loadImageLib("assets/graphics/libs/ghost_negative/ghost.xml");
        IMGLIB_EFFECTS = aGame.loadImageLib("assets/graphics/libs/effects/effects.xml");
        IMGLIB_NUMBER_ONE = aGame.loadImageLib("assets/graphics/libs/number_one/number_one.xml");
        IMGLIB_NUMBER_ONE_NEGATIVE = aGame.loadImageLib("assets/graphics/libs/number_one_negative/number_one.xml");
        IMGLIB_MISC = aGame.loadImageLib("assets/graphics/libs/misc/misc.xml");
        
        global SND_GHOST_DAMAGE;
        global SND_GHOST_LAUGH;
        global SND_GHOST_DEAD;
        global SND_ATTACK_LAUNCH;
        global SND_NUMBER_ONE_DAMAGE;
        global SND_DIAMOND_BOUNCE;
        global SND_DIAMOND_GET;
        global SND_CLOCK_PAIR;
        global SND_CLOCK_UNPAIR;
        global SND_NOZAR_APPEAR;
        
        SND_GHOST_DAMAGE = aGame.loadSound("assets/audio/sfx/ghost_damage.wav");
        SND_GHOST_LAUGH = aGame.loadSound("assets/audio/sfx/ghost_laugh.wav");
        SND_GHOST_DEAD = aGame.loadSound("assets/audio/sfx/ghost_dead.wav");
        SND_ATTACK_LAUNCH = aGame.loadSound("assets/audio/sfx/magic_throw.wav");
        SND_NUMBER_ONE_DAMAGE = aGame.loadSound("assets/audio/sfx/number_one_damage.wav");
        SND_DIAMOND_BOUNCE = aGame.loadSound("assets/audio/sfx/diamond_bounce.wav");
        SND_DIAMOND_GET = aGame.loadSound("assets/audio/sfx/diamond_get.wav");
        SND_CLOCK_PAIR = aGame.loadSound("assets/audio/sfx/clock_pair.wav");
        SND_CLOCK_UNPAIR = aGame.loadSound("assets/audio/sfx/clock_unpair.wav");
        SND_NOZAR_APPEAR = aGame.loadSound("assets/audio/sfx/nozar_appear.wav");
        
    @staticmethod
    def updateKeys(aKeys):
        global KEY_STATE_PREV;
        global KEY_STATE;
        KEY_STATE_PREV = KEY_STATE;
        KEY_STATE = aKeys;
        
        
        CTRL1.updateWithKeys(aKeys, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l);
        
class Keyboard:
    @staticmethod
    def isPressed(aKey):
        return KEY_STATE[aKey] and not KEY_STATE_PREV[aKey];
    @staticmethod
    def isDown(aKey):
        return KEY_STATE[aKey];

'''
    GAME CLASSES
'''
   
class SimpleState:
    def __init__(self):
        self.effects = list();
        self.game = None;
        self.time = 0;
        pass;
    
    def init(self, aGame):
        self.game = aGame;
        pass;
    
    def update(self):
        
        self.time += 1;
        
        for eff in self.effects:
            eff.update();
            if eff.dead:
                self.effects.remove(eff);
        
        pass;
    
    def render(self, aGame):
        assert isinstance(aGame,game.Game);
        
        for eff in self.effects:
            eff.render(aGame);
        
        
        pass;
    
    def spawnEffect(self, aEffect):
        self.effects.append(aEffect);
        pass;
    
    def killEffects(self):
        self.effects[:] = [];

class TextState(SimpleState):
    
    def __init__(self):
        SimpleState.__init__(self);
        
        self.steps = list();
        self.currentStep = 0;
        self.textLines = list();
        self.skipTime = 0;
        self.textCenterX = 300/2;
        self.textCenterY = 225/2;
        self.creditMode = False;
    
    def addStep(self, aTime):
        aTime *= 60;
        
        if len(self.steps) > 0:
            aTime += self.steps[len(self.steps) - 1];
            
        self.steps.append(int(aTime));
    
    def init(self, aGame):
        assert isinstance(aGame,game.Game);
        SimpleState.init(self, aGame);
        
    def update(self):
        SimpleState.update(self);
        
        if self.skipTime > 0:
            self.skipTime -= 1;
            if Keyboard.isPressed(pygame.K_RETURN) or Keyboard.isPressed(pygame.K_ESCAPE):
                self.onEnterStep(-1);
                return;
        elif Keyboard.isPressed(pygame.K_RETURN) or Keyboard.isPressed(pygame.K_ESCAPE):
            self.skipTime = 60;
        
        if self.currentStep >= len(self.steps):
            self.onEnterStep(-2);
            return;
        
        if self.time > self.steps[self.currentStep]:
            self.onEnterStep(self.currentStep);
            self.currentStep += 1;
            
        y = self.textCenterY - (len(self.textLines) * 10)/2;
        
        if self.creditMode:
            y = 225;
            for line in self.textLines:
                self.spawnEffect(FloatString(line, self.textCenterX, y, -0.5, 1, 99999999999));
                y += 10;
        else:
            for line in self.textLines:
                self.spawnEffect(FloatString(line, self.textCenterX, y, -1, 0.9, 99999999999));
                y += 10;
            
        self.textLines[:] = [];
        
        
        
    def onEnterStep(self, aStep):
        if aStep != -1 and not self.creditMode:
            for eff in reversed(self.effects):
                if isinstance(eff, FloatString):
                    self.effects.remove(eff);
        pass;
    
    def write(self, aText):
        self.textLines.append(aText);
        
    def render(self, aGame):
        assert isinstance(aGame,game.Game);
        SimpleState.render(self, aGame);
        
        
        if self.skipTime > 0:
            aGame.drawCenteredText(FNT_CLEARLY_DARK, 200, 195, "PRESS ENTER OR ESCAPE");
            aGame.drawCenteredText(FNT_CLEARLY_DARK, 200, 205, "TO SKIP THIS ->");

class PrologueState(TextState):
    def __init__(self):
        TextState.__init__(self);
        self.addStep(1);
        
        
        
        
        
        
        self.addStep(3);
        self.addStep(2);
        self.addStep(3);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(3);
        self.addStep(3);
        self.addStep(3);
        self.addStep(3);
        self.addStep(5);
        self.addStep(5);
        self.addStep(8);
        self.addStep(5);
        self.addStep(8);
        self.addStep(5);
        self.addStep(5);
        self.addStep(5);
        self.addStep(3);
        self.addStep(3);
        
        self.fairyAppear = False;
        
    def init(self, aGame):
        assert isinstance(aGame,game.Game);
        
        TextState.init(self, aGame);
        
        aGame.setBackground("assets/graphics/bg/black_screen.png");
        aGame.stopMusic();
        
    def onEnterStep(self, aStep):
        
        TextState.onEnterStep(self, aStep);
        
        #TODO: Translate (INTRO)
        if aStep == 0:
            self.write("ERA UN DiA COMO CUALQUIER OTRO...");
        elif aStep == 1:
            self.write("   HASTA QUE...");
        elif aStep == 2:
            self.write("^UNA TORRE SURGIo DE LAS");
            self.write("PROFUNIDADES DE LA TIERRA!");
            self.game.playMusic("assets/audio/bgm/prologue.ogg");
        elif aStep == 3:
            self.write("DERREPENTE COMENZARON A SALIR");
            self.write("FANTASMAS DE ELLA");
            self.write("QUE ASUSTABAN A LA GENTE");
        elif aStep == 4:
            self.write("NADIE SE ANIMABA A ENTRAR A");
            self.write("   LA TORRE HASTA QUE...");
            
        elif aStep == 5:
            self.write("UN VALIENTE NInO POR FIN");
            self.write("   SE ATREVIo A HACERLO...");
            self.game.stopMusic();
            
        elif aStep == 6:
            self.write("   ESTANDO DENTRO DE LA TORRE...");
            self.game.setBackground("assets/graphics/bg/tower_cutscene_1.png");
            self.game.playMusic("assets/audio/bgm/mystery.ogg");
        elif aStep == 7:
            self.write("eL ESCUCHo UNA VOZ");
        elif aStep == 8:
            self.fairyAppear = True;
            self.write("^HOLA!");
        elif aStep == 9:
            self.textCenterY = 225 - 225/3;
            self.write("ES RARO VER A UNA PERSONA POR AQUi.");
        elif aStep == 10:
            self.write("MI NOMBRE ES ARIA.");
        elif aStep == 11:
            self.write("ESTA TORRE ESTA CONTROLADA POR UN");
            self.write("MAGO LLAMADO NOZAR.");
        elif aStep == 12:
            self.write("SI QUIERES DETENERLO A eL Y A");
            self.write("SUS FANTASMAS, YO PUEDO AYUDARTE.");
        elif aStep == 13:
            self.write("TENEMOS QUE LLEGAR AL PISO MaS ALTO.");
            self.write("PERO PARA HACERLO, NECESITAMOS");
            self.write("LOS 15 DIAMANTES DE CADA PISO.");
        elif aStep == 14:
            self.write("EL PROBLEMA, ES QUE ESOS DIAMANTES");
            self.write("LOS TIENEN LOS FANTASMAS.");
        elif aStep == 15:
            self.write("POR ESO, TE DARe ESTOS BRAZALETES");
            self.write("MaGICOS, QUE TE PERMITIRaN");
            self.write("HACERLOS DESAPARCER POR");
            self.write("UNOS SEGUNDOS.");
        elif aStep == 16:
            self.write("ESE MOMENTO, DEBERaS APROVECHARLO");
            self.write("PARA CONSEGUIR LOS DIAMANTES");
        elif aStep == 17:
            self.write("INTENTA NO DEMORARTE MUCHO");
            self.write("SI NOZAR SE ENTERA");
            self.write("QUE ESTAMOS AQUi...");
        elif aStep == 18:
            self.write("PODRiA HACERSE CON LOS DIAMANTES.");
            self.write("Y NO PODRiAMOS HACERLE FRENTE.");
        elif aStep == 19:
            self.write("&ESTaS LISTO?");
        elif aStep == 20:
            self.write("^VAMOS POR NOZAR ENTONCES!");
        elif aStep == -1 or aStep == 21:
            #TODO:Test Stages Here
            self.game.nextState = IntermisionState(0);
            #self.game.nextState = IntermisionState(5);
            #self.game.nextState = EndingState();
            
    def render(self, aGame):
        
        assert isinstance(aGame, game.Game);
        if self.fairyAppear:
            aGame.drawImage(IMGLIB_MISC.images["fairy"], 0, math.sin(self.time / 60) * 4, False);
        
        TextState.render(self, aGame);
            
class EndingState(TextState):
    def __init__(self):
        TextState.__init__(self);
        self.addStep(1);
        
        
        
        self.addStep(3);
        self.addStep(3);
        self.addStep(3);
        self.addStep(3);
        self.addStep(3);
        self.addStep(9);
        self.addStep(3);
        self.addStep(7);
        self.addStep(7);
        self.addStep(3);
        self.addStep(3);
        self.addStep(5);
        self.addStep(3);
        self.addStep(9);
        self.addStep(6);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(4);
        self.addStep(10);
        
    def init(self, aGame):
        assert isinstance(aGame,game.Game);
        
        TextState.init(self, aGame);
        
        aGame.setBackground("assets/graphics/bg/black_screen.png");
        aGame.stopMusic();
        
    def onEnterStep(self, aStep):
        
        if aStep == -2:
            self.skipTime = 10;
            return;
        
        TextState.onEnterStep(self, aStep);
        
        #TODO: Translate (ENDING)
        if aStep == 0:
            self.write("EL MOMENTO DE LA VERDAD");
            self.write("POR FIN HABiA LLEGADO...");
        elif aStep == 1:
            self.write("^NUESTRO HeROE, CARA A CARA");
            self.write("FRENTE A NOZAR!");
        elif aStep == 2:
            self.write("&AMERITABA ESTO UNA VENGANZA?");
        elif aStep == 3:
            self.write("   eL NO LO CREYo ASi...");
        elif aStep == 4:
            self.write("LA TORRE DE NOZAR NO HABiA");
            self.write("HECHO NINGuN MAL.");    
        elif aStep == 5:
            self.write("LOS FANTASMAS ERAN INOFENSIVOS,");
            self.write("MaS AuN, TANTO LOS FANTASMAS");
            self.write("COMO NOZAR, SOLO QUERiAN");
            self.write("UNA COSA...");
        elif aStep == 6:
            self.write("E N S E n A R N O S");
        elif aStep == 7:
            self.write("NUESTRO AMIGO, LO COMPRENDIo...");
            self.write("EL DESAFiO QUE NOZAR LE HA");
            self.write("PUESTO, HA SIDO MUY DIVERTIDO");
        elif aStep == 8:
            self.write("LA GENTE TEME A LO QUE DESCONOCE...");
            self.write("PERO AHORA, LOS NuMEROS YA NO SERaN");
            self.write("UN MISTERIO PARA eL");
        elif aStep == 9:
            self.write("   ENTONCES...");
        elif aStep == 10:
            self.write("&QUe HARa AHORA?");
        elif aStep == 11: 
            self.write("&LE PEDIRa A NOZAR QUE VUELVA");
            self.write("A ESCONDER LA TORRE BAJO LA TIERRA?");
        elif aStep == 12:
            self.write("^POR SUPUESTO QUE NO!");
        elif aStep == 13:
            self.write("NUESTRO AMIGO HA ENTENDIDO,");
            self.write("LE HA DADO LAS GRACIAS A NOZAR,");
            self.write("Y SE HA MARCHADO.");
        elif aStep == 14:
            self.write("NO SIN ANTES, INTERCAMBIAR CON");
            self.write("NOZAR, EL HADA Y ALGUNOS FANTASMAS");
            self.write("SUS DIRECCIONES DE MAIL Y TWITTER");
            self.game.playMusic("assets/audio/bgm/torre_de_nozar_credits.ogg");
            
        elif aStep == 15:
            self.creditMode = True;
            self.killEffects();
            self.write("CReDITOS");
            self.write(" ");
            self.write("PROYECTO -LA TORRE DE NOZAR-");
        elif aStep == 16:
            self.write("IDEA ORIGINAL Y DISEnO");
            self.write(" ");
            self.write("-SEBASTIaN GARCiA-");
        elif aStep == 17:
            self.write("PROGRAMACIoN");
            self.write(" ");
            self.write("-SEBASTIaN GARCiA-");
        elif aStep == 18:
            self.write("GRaFICOS");
            self.write(" ");
            self.write("-SEBASTIaN GARCiA-");
        elif aStep == 19:
            self.write("SONIDO Y MuSICA");
            self.write(" ");
            self.write("-SEBASTIaN GARCiA-");
        elif aStep == 20:
            self.write("ASESORAMIENTO PEDAGoGICO");
            self.write(" ");
            self.write("-GISELLE RUIZ-");
        elif aStep == 21:
            self.write("CALIBRACIoN DE NIVELES");
            self.write(" ");
            self.write("-GISELLE RUIZ-");
        elif aStep == 22:
            self.creditMode = False;
            self.write("HTTP://SEBAGAMES.NET");
            self.write(" ");
            self.write("^GRACIAS POR JUGAR!");
        elif aStep == -1:
            self.game.nextState =  TitleState();
            
        
        
class TitleState:
    def __init__(self):
        self.game = None;
        self.time = 0;
        self.startTime = 480;
        self.inputStartTime = self.startTime + 120;
        self.isShowBackground = False;
    
    def init(self, aGame):
        assert isinstance(aGame,game.Game);
        
        self.game = aGame;
        
        aGame.setBackground("assets/graphics/bg/black_screen.png");
        aGame.playMusic("assets/audio/bgm/torre_de_nozar.ogg");
    
    def update(self):
        g = self.game;
        assert isinstance(g,game.Game);
        
        self.time += 1;
        
        if self.time > self.startTime:
            if not self.isShowBackground:
                g.setBackground("assets/graphics/bg/title.png");
                self.isShowBackground = True;
            if self.time > self.inputStartTime:
                if Keyboard.isPressed(pygame.K_RETURN):
                    g.nextState = PrologueState();
        else:
            if Keyboard.isPressed(pygame.K_RETURN):
                self.time = self.inputStartTime;
    
    def render(self, aGame):
        assert isinstance(aGame,game.Game);
        
        if self.time < self.startTime:
            aGame.drawCenteredText(FNT_CLEARLY, 150, 225/2, "SEBAGAMES PRESENTS");
            if self.time > self.startTime - 120:
                aGame.drawCenteredText(FNT_CLEARLY, 150, 225/2 + 20, "A SEBAGAMES PRODUCTION");
        
        if self.time > self.inputStartTime:
            if self.time % 60 < 40:
                aGame.drawCenteredText(FNT_CLEARLY, 150, 170, "PRESS ENTER TO PLAY");
        
class IntermisionState(TextState):
    def __init__(self, aLevelIndex):
        TextState.__init__(self);
        self.addStep(1);
        self.addStep(3);
        self.addStep(4);
        self.levelIndex = aLevelIndex;
        self.textCenterX = 180;
        self.textCenterY = 225 - 225/3;
        
    def init(self, aGame):
        TextState.init(self, aGame);
        aGame.setBackground("assets/graphics/bg/intermission.png");
        
    def onEnterStep(self, aStep):
        TextState.onEnterStep(self, aStep);
        
        #TODO: Translate (INTERMISION)
        if aStep == 0:
            if self.levelIndex == 0:
                self.write("^ESTAMOS EN EL PRIMER PISO!");
            else:
                self.write("^SUBIMOS AL PISO " + str(self.levelIndex + 1) + "!");
        elif aStep == 1:
            rest = len(levels.LIST) - (self.levelIndex);
            
            if rest == 1:
                self.write("^SOLO NOS FALTA ESTE PISO");
            elif rest > 1:
                self.write("^SOLO NOS FALTAN " + str(rest) + " PISOS");
                
            self.write("PARA LLEGAR A LA CIMA!");
        elif aStep == 2 or aStep == -1:
            self.game.nextState = GameplayState(self.levelIndex);
        
    def render(self, aGame):
        assert isinstance(aGame, game.Game);
        aGame.drawImage(IMGLIB_MISC.images["fairy"], 0, math.sin(self.time / 60) * 4, False);
        TextState.render(self, aGame);
        
        
        
class GameplayState:
    def __init__(self, aLevelIndex = 0):
        
        self.levelIndex = aLevelIndex;
        
        self.secondCounter = 0;
        self.paused = False;
        self.game = None;
        
        self.mainCharacter = None;
        self.attack = None;
        
        self.plusValue = 1;
        self.minusValue = 1;
        self.divideValue = 2;
        
        self.timeOverEffect = None;
        
        self.pauseOption = 0;
        self.pauseSubMenu = 0;
            
        self.drawableEntities = [];
        
        self.ghosts = [];
        
        self.enemyAmount = 0;
        
        self.hudDiamonds = list();
        for i in range(0,15):
            self.hudDiamonds.append(HudDiamond(246 + (i % 5) * 8, 22 + int(i / 5) * 8, 60 - i * 4));
            
        self.diamondCount = 0;
        
        self.freeDiamonds = list();
        self.maxFreeDiamonds = 3;
        
        self.numberOnes = list();
        
        self.effects = list();
        self.hudEffects = list();
        
        self.time = 0;
        
        self.levelCurrentGhostIndex = 0;
        self.currentLevel = levels.LIST[self.levelIndex];
        
        self.SEQUENCE_INTRO = 0;
        self.SEQUENCE_GAMEPLAY = 1;
        self.SEQUENCE_WIN = 2;
        self.sequence = self.SEQUENCE_INTRO;
        self.sequenceTime = 0;
        
    
    def init(self, aGame):
        assert isinstance(aGame,game.Game);
        self.game = aGame;

        self.mainCharacter = MainCharacter(100, 0, 100, 1, CTRL1, self);
        aGame.setBackground("assets/graphics/bg/bg" + str(int((self.levelIndex)/2)%4 + 1) + ".png");
        aGame.stopMusic();
        
        self.reset();
        
        if self.currentLevel.plusNumber == 0:
            self.plusValue = random.randint(1,9);
        else:
            self.plusValue = self.currentLevel.plusNumber;
        
        if self.currentLevel.minusNumber == 0:
            self.minusValue = random.randint(1,9);
        else:
            self.minusValue = self.currentLevel.minusNumber;
  
    def reset(self):
        self.timeOverEffect = None;
        self.time = self.currentLevel.totalSeconds;
        self.enemyAmount = self.currentLevel.enemyAmount;
        self.levelCurrentGhostIndex = 0;
        
        
    def update(self):
        
        g = self.game;
        assert isinstance(g, game.Game);
            
        if self.paused:
            
            if Keyboard.isPressed(pygame.K_DOWN) or Keyboard.isPressed(pygame.K_UP) or Keyboard.isPressed(pygame.K_k) or Keyboard.isPressed(pygame.K_i):
                g.playSound(SND_DIAMOND_BOUNCE);
                if self.pauseOption == 0:
                    self.pauseOption = 1;
                else:
                    self.pauseOption = 0;
                    
            if Keyboard.isPressed(pygame.K_RETURN):
                if self.pauseOption == 0:
                    self.paused = False;
                    g.playSound(SND_CLOCK_UNPAIR);
                else:
                    if self.pauseSubMenu == 0:
                        self.pauseSubMenu = 1;
                        self.pauseOption = 0;
                        g.playSound(SND_CLOCK_UNPAIR);
                    else:
                        self.game.nextState = TitleState();
            elif Keyboard.isPressed(pygame.K_ESCAPE):
                self.paused = False;
                g.playSound(SND_CLOCK_UNPAIR);
                
            
        else:
            
            if Keyboard.isPressed(pygame.K_RETURN) or Keyboard.isPressed(pygame.K_ESCAPE):
                self.paused = True;
                self.pauseOption = 0;
                self.pauseSubMenu = 0;
                g.playSound(SND_CLOCK_PAIR);
                
                return;
            
            if self.sequence == self.SEQUENCE_INTRO:
                
                self.sequenceTime += 1;
                
                initialWait = -570;
                if self.levelIndex == 0:
                    initialWait = 30;
                
                #TODO: Translate (HELP)
                if self.sequenceTime == initialWait:
                    self.spawnHudEffect(FloatString("LLEVA EL NuMERO DE", 150, 80, -2, 0.8, 300));
                if self.sequenceTime == initialWait + 10:
                    self.spawnHudEffect(FloatString("LOS FANTASMAS A CERO", 150, 90, -2, 0.8, 300 - 10));
                if self.sequenceTime == initialWait + 20:
                    self.spawnHudEffect(FloatString("PARA CONSEGUIR 15 DIAMANTES", 150, 100, -2, 0.8, 300 - 20));
                if self.sequenceTime == initialWait + 30:
                    self.spawnHudEffect(FloatString("ANTES QUE EL TIEMPO ACABE", 150, 110, -2, 0.8, 300 - 30));
                    
                elif self.sequenceTime == 350 + initialWait:
                    self.spawnHudEffect(FloatString("CAMINA USANDO LAS TECLAS: I,J,K,L", 150, 80, -2, 0.8, 220));
                elif self.sequenceTime == 350 + initialWait + 10:
                    self.spawnHudEffect(FloatString("Y USA TUS PODERES CON: z,x,c", 150, 90, -2, 0.8, 220 - 10));
                
                elif self.sequenceTime == 600 + initialWait:
                    self.spawnHudEffect(FloatString("AHORA TUS PODERES SON:", 30, 80, -2, 0.8, 270, False));
                elif self.sequenceTime == 630 + initialWait:
                    self.spawnHudEffect(FloatString("zDICIoN: " + str(self.plusValue), 150, 100, -2, 0.8, 240, False));
                elif self.sequenceTime == 640 + initialWait:
                    self.spawnHudEffect(FloatString("xUSTRACCIoN: " + str(self.minusValue), 140, 110, -2, 0.8, 230, False));
                elif self.sequenceTime == 650 + initialWait:
                    self.spawnHudEffect(FloatString("cIVISIoN: 2", 130, 120, -2, 0.8, 220, False));
                elif self.sequenceTime == 890 + initialWait:
                    self.spawnHudEffect(FloatString("VERIFiCALOS ARRIBA SI TIENES DUDAS", 150, 60, -2, 0.8, 140));
                elif self.sequenceTime == 1070 + initialWait:
                    self.spawnHudEffect(FloatString("&ESTaS PREPARADO?", 150, 80, -2, 0.8, 60));
                elif self.sequenceTime == 1160 + initialWait:
                    self.spawnHudEffect(FloatString("^ADELANTE!", 150, 100, -2, 0.8, 60));
                    self.sequence = self.SEQUENCE_GAMEPLAY;
                    self.game.playMusic("assets/audio/bgm/torre_de_nozar_gameplay.ogg");
                    
            elif self.sequence == self.SEQUENCE_GAMEPLAY:
                if self.timeOverEffect == None and self.isLoseCondition():
                    self.timeOverEffect = NozarTimeUpEffect(self);
                
                if self.time > 0 and not self.isWinCondition():
                    self.secondCounter += 1;
                    if self.secondCounter >= 60:
                        self.secondCounter -= 60;
                        self.time -= 1;
                        if self.time == 30:
                            #TODO: Translate
                            self.spawnHudEffect(FloatString("^NOZAR LLEGARa EN 30 SEGUNDOS!", 150, 40, 4, 0.75, 60 * 3));
                        
                        if self.time <= 10:
                            if self.time == 10:
                                self.game.stopMusic();
                                #TODO: Translate
                                self.spawnHudEffect(FloatString("^RaPIDO, EL TIEMPO SE ACABA!", 150, 40, 4, 0.75, 60 * 3));
                            if self.time % 2 == 0:
                                self.playSound(SND_CLOCK_PAIR);
                                
                            else:
                                self.playSound(SND_CLOCK_UNPAIR);
                        if self.time == 0:#Make all ghosts, number ones and free diamonds disappear
                            self.emptyLevel();
                            
                
                
                if self.isWinCondition():
                    self.emptyLevel();
                    if self.isEmptyLevel() and self.mainCharacter.state != self.mainCharacter.ST_WIN:
                        self.mainCharacter.setState(self.mainCharacter.ST_WIN);
                        self.spawnHudEffect(FloatString("VERY WELL!", 150, 75, -2, 0.9, 60));
                    
                    if self.mainCharacter.readyToNextLevel:
                        
                        self.sequenceTime = 0;
                        self.sequence = self.SEQUENCE_WIN;
                        
                while len(self.ghosts) < self.enemyAmount:
                    self.spawnNextGhost();
                    
            elif self.sequence == self.SEQUENCE_WIN:
                
                self.sequenceTime += 1;
                if self.sequenceTime == 60:
                    if self.levelIndex + 1 == len(levels.LIST):
                        self.game.nextState = EndingState();
                    else:
                        self.game.nextState = IntermisionState((self.levelIndex + 1));
                        
                            
            self.mainCharacter.update();
            
            if self.attack != None:
                self.attack.update();
                
            
                
                
            for ghost in self.ghosts:
                ghost.update();
                
            for ghost in reversed(self.ghosts):
                if ghost.isDead():
                    self.ghosts.remove(ghost);
                    
            for numberOne in self.numberOnes:
                numberOne.update();
                
            for numberOne in reversed(self.numberOnes):
                if numberOne.dead:
                    self.numberOnes.remove(numberOne);
            
            
            for diamond in self.freeDiamonds:
                diamond.update();
                #check contact with player
                if abs(self.mainCharacter.gameObj.x - diamond.gameObj.x) < 16:
                    if abs(self.mainCharacter.gameObj.z - diamond.gameObj.z) < 24:
                        if abs(self.mainCharacter.gameObj.y - diamond.gameObj.y) < 32:
                            diamond.take(True); 
                
            for diamond in reversed(self.freeDiamonds):
                if diamond.dead:
                    self.freeDiamonds.remove(diamond);
            
                    
            for hudDiamond in self.hudDiamonds:
                hudDiamond.update();
            
            for effect in self.effects:
                effect.update();
            
            for effect in reversed(self.effects):
                if effect.dead:
                    self.effects.remove(effect);
                
            for effect in self.hudEffects:
                effect.update();
            
            for effect in reversed(self.hudEffects):
                if effect.dead:
                    self.hudEffects.remove(effect);
                    
            if self.timeOverEffect != None:
                self.timeOverEffect.update();
                if self.timeOverEffect.dead:
                    self.reset();
                    self.game.playMusic("assets/audio/bgm/torre_de_nozar_gameplay.ogg");
        
    def render(self, aGame):
        
        assert isinstance(aGame, game.Game);
        
        #Clear all drawable entities
        del self.drawableEntities[0:len(self.drawableEntities)];
        
        #Add character to drawable entities
        self.drawableEntities.append(self.mainCharacter);
        
        if self.attack != None:#Add attack to drawable entities if exists
            self.drawableEntities.append(self.attack);
            
        #Add ghosts from their list
        for ghost in self.ghosts:
            self.drawableEntities.append(ghost);
            
        #Add number ones
        for numberOne in self.numberOnes:
            self.drawableEntities.append(numberOne);
            
        #Add diamonds
        for diamond in self.freeDiamonds:
            self.drawableEntities.append(diamond);
            
        #Add effects
        for effect in self.effects:
            self.drawableEntities.append(effect);
        
        #Sort drawable entities characters:
        #sorted(self.drawableEntities, key=lambda obj: obj.getDepth());
        self.drawableEntities.sort(cmp=None, key = lambda obj: obj.getDepth(), reverse = False)
        
        for entity in self.drawableEntities:
            entity.render(aGame);
        
        
        #DRAW HUD
        aGame.drawText(FNT_CLEARLY, 39, 12, str(self.plusValue));
        aGame.drawText(FNT_CLEARLY, 39, 25, str(self.minusValue));
        
        #Draw level Number
        lvX = 177;
        if self.levelIndex + 1 > 9:
            lvX -= FNT_CLEARLY.charSize[0];
        aGame.drawText(FNT_CLEARLY, lvX, 10, str(self.levelIndex + 1));
        aGame.drawText(FNT_CLEARLY, 201, 10, str(len(levels.LIST)));
        
        #Draw time
        minutesLeft = int(self.time / 60);
        if minutesLeft < 10:
            strMinutes = "0" + str(minutesLeft);
        else:
            strMinutes = str(minutesLeft);
            
        secondsLeft = self.time % 60;
        if secondsLeft < 10:
            strSeconds = "0" + str(secondsLeft);
        else:
            strSeconds = str(secondsLeft);
            
        aGame.drawText(FNT_TIME, 176, 30, strMinutes);
        aGame.drawText(FNT_TIME, 196, 30, strSeconds);
        
        if self.timeOverEffect != None:
            self.timeOverEffect.render(aGame);
        
        for hudDiamond in self.hudDiamonds:
            hudDiamond.render(aGame);
            
        for effect in self.hudEffects:
            effect.render(aGame);
        
        if self.paused:
            aGame.drawImage(IMGLIB_MISC.images["pause_portrait"], 0, 0, False);
            if self.pauseSubMenu == 0:
                aGame.drawCenteredText(FNT_CLEARLY, 150, 86, "PAUSE!");
                if self.pauseOption == 0:
                    aGame.drawCenteredText(FNT_CLEARLY, 150, 110, "<RESUME>");
                    aGame.drawCenteredText(FNT_CLEARLY_DARK, 150, 122, "BACK TO TITLE");
                else:
                    aGame.drawCenteredText(FNT_CLEARLY_DARK, 150, 110, "RESUME");
                    aGame.drawCenteredText(FNT_CLEARLY, 150, 122, "<BACK TO TITLE>");
            else:
                aGame.drawCenteredText(FNT_CLEARLY, 150, 86, "ARE YOU SURE?");
                if self.pauseOption == 0:
                    aGame.drawCenteredText(FNT_CLEARLY, 150, 110, "<NO>");
                    aGame.drawCenteredText(FNT_CLEARLY_DARK, 150, 122, "OF COURSE!");
                else:
                    aGame.drawCenteredText(FNT_CLEARLY_DARK, 150, 110, "NO");
                    aGame.drawCenteredText(FNT_CLEARLY, 150, 122, "<OF COURSE!>");
                    
                
        
        #aGame.drawText(FNT_CLEARLY, 8, 120, "0123456789+-%:=,#.ABCDEFGHIJKLMNn#OPQRSTUVWXYZaeio#u!^?&`';y");
        #aGame.drawText(FNT_CLEARLY, 180, 200, "RENDERS: " + str(aGame.lastDrawInstructionCount));
        
    
    def isLoseCondition(self):
        return self.time == 0 and len(self.ghosts) == 0 and len(self.freeDiamonds) == 0 and not self.isWinCondition();
    
    def isWinCondition(self):
        return self.diamondCount == len(self.hudDiamonds);
    
    
    def emptyLevel(self):
        self.enemyAmount = 0;
        for ghost in self.ghosts:
            if ghost.state != ghost.ST_DEAD:
                ghost.dropValue = 0;
                ghost.setState(ghost.ST_DEAD);
                
        for numberOne in self.numberOnes:
            if numberOne.state != numberOne.ST_DEADING:
                numberOne.setState(numberOne.ST_DEADING);    
            
        for diamond in self.freeDiamonds:
            diamond.dead = True;
            self.spawnEffect(SimpleAnimEffect(ANIM_SPARK, diamond.gameObj.x, diamond.gameObj.y, diamond.gameObj.z, choice((True,False)), (pygame.BLEND_ADD)));
    
    def isEmptyLevel(self):
        return len(self.ghosts) == 0 and len(self.numberOnes) == 0 and len(self.freeDiamonds) == 0;
    
    def spawnPlayerAttack(self, aOperator):
        
        if aOperator == "+":
            self.attack = Attack(self.mainCharacter.gameObj.x + self.mainCharacter.direction * 16, self.mainCharacter.gameObj.z, self.mainCharacter.direction, self.plusValue, "+", self);
        elif aOperator == "-":
            self.attack = Attack(self.mainCharacter.gameObj.x + self.mainCharacter.direction * 16, self.mainCharacter.gameObj.z, self.mainCharacter.direction, self.minusValue, "-", self);
        elif aOperator == "/":
            self.attack = Attack(self.mainCharacter.gameObj.x + self.mainCharacter.direction * 16, self.mainCharacter.gameObj.z, self.mainCharacter.direction, self.divideValue, "/", self);


    def spawnNextGhost(self):
        life = self.currentLevel.ghostEntries[self.levelCurrentGhostIndex % len(self.currentLevel.ghostEntries)];
        drop = 0;
        if self.levelCurrentGhostIndex % self.currentLevel.ghostsDefeatedForDiamondDrop == 0:
            drop = self.currentLevel.diamondDropAmount;
        self.spawnGhosts(life, random.randint(GAME_LIMIT_LEFT, GAME_LIMIT_RIGHT), random.randint(GAME_LIMIT_BACK, GAME_LIMIT_FRONT), choice((-1,1)), drop);
        self.levelCurrentGhostIndex += 1;

    def spawnGhosts(self, aLife, aX, aZ, aDirection, aDropValue):
        if aLife == 0:
            aLife = random.randint(1,20) * choice((1,-1));
        
        self.ghosts.append(Ghost(aX, aZ, aDirection, self, aLife, aDropValue));
                
    def getDiamond(self, aX, aY):
        if self.diamondCount >= len(self.hudDiamonds):
            return False;
        
        self.hudDiamonds[self.diamondCount].moveToDestination(aX, aY, 60);
        self.diamondCount += 1;
        return True;
        
    def leftDiamond(self, aFromX, aFromY, aFrames):
        if self.diamondCount == 0:
            return False;
        
        self.diamondCount -= 1;
        self.hudDiamonds[self.diamondCount].leftFromCurrent(aFromX, aFromY, aFrames);
        return True;
    
    def spawnDiamond(self, aX, aY, aZ):
        if self.diamondCount + len(self.freeDiamonds) >= len(self.hudDiamonds):
            return;
        self.freeDiamonds.append(Diamond(aX, aY, aZ, self));
        
    def spawnNumberOne(self, aX, aZ, aDirection, aNegative):
        
        if len(self.numberOnes) > 3:
            oldest = None;
            for n in self.numberOnes:
                if n.state != n.ST_DEADING:
                    if oldest == None or n.totalTime > oldest.totalTime:
                        oldest = n;
                        
            if oldest != None:
                oldest.setState(oldest.ST_DEADING);
                
        self.numberOnes.append(NumberOne(aX, aZ, aDirection, aNegative, self));
        
    def getStillDiamondPos(self):
        for d in self.freeDiamonds:
            if abs(d.gameObj.velX) < 0.1 and abs(d.gameObj.velY) < 0.1 and abs(d.gameObj.velZ) < 0.1 and d.gameObj.y > -10:
                return (d.gameObj.x, d.gameObj.z); 
        return None;
    
    def tryStealDiamond(self, aX, aZ):
        for d in self.freeDiamonds:
            if d.gameObj.y > -10 and abs(aX - d.gameObj.x) < 16 and abs(aZ - d.gameObj.z) < 16:
                d.take(False);
                return True;
            
        return False;
    
    def playSound(self, aSnd):
        self.game.playSound(aSnd);
        
    def spawnEffect(self, aEffect):
        self.effects.append(aEffect);
        
    def spawnHudEffect(self, aEffect):
        self.hudEffects.append(aEffect);
        
            

class GameCharacter:
    
    def __init__(self, aX, aY, aZ, aDirection, aCtrl, aImgLib, aManager):
        self.gameObj = GameObject();
        self.gameObj.x = aX;
        self.gameObj.y = aY;
        self.gameObj.z = aZ;
        self.direction = aDirection;
        self.state = self.ST_NULL;
        self.control = aCtrl;
        self.stateTime = 0;
        self.imgLib = aImgLib;
        self.manager = aManager;
        self.shakeTime = 0;
        
    def update(self):
        self.gameObj.update();
        
        if self.gameObj.pauseTime == 0:
            self.updateState();
            
            if self.shakeTime > 0:
                self.shakeTime -= 1;
            
            
    def render(self, aGame):
        if self.imgLib != None:
            if self.direction == -1:
                mirror = True;
            else:
                mirror = False;
            aGame.drawImage(self.imgLib.images[self.gameObj.currentFrame], self.gameObj.x, self.getDrawY(), mirror);
            
    def updateState(self):
        self.stateTime += 1;
        self.state();
    
    def setState(self, aStMethod):
        self.state = aStMethod;
        self.stateTime = 0;
        self.onSetState();
        
    def onSetState(self):
        return;
    
    def turnLogic(self):
        if self.control.back(self.direction):
            self.direction = -self.direction;
            
    def stopMovement(self):
        self.gameObj.velX = 0.0;
        self.gameObj.velZ = 0.0;
        
    def getDepth(self):
        return self.gameObj.z;
    
    def getDrawY(self):
        return self.gameObj.getDrawY();
        
    def ST_NULL(self):
        return;
    
class MainCharacter(GameCharacter):
    def __init__(self, aX, aY, aZ, aDirection, aCtrl, aManager):
        GameCharacter.__init__(self, aX, aY, aZ, aDirection, aCtrl, IMGLIB_CHARACTER, aManager);
        self.readyToNextLevel = False;
        self.setState(self.ST_STAND);
        
        self.fairyOffset = 0;
        
        self.fairyTime =0;
        
        return;
    
    def update(self):
        GameCharacter.update(self);
        
        self.fairyTime += 1;
        
        self.fairyOffset -= self.direction * 8;
        if self.fairyOffset < -32:
            self.fairyOffset = -32;
        elif self.fairyOffset > 32:
            self.fairyOffset = 32;
    
    def render(self, aGame):
        assert isinstance(aGame,game.Game);
        
        GameCharacter.render(self, aGame);
        
        fairyImg = "fairy0";
        if self.fairyTime % 8 <= 4:
            fairyImg += "0";
        else:
            fairyImg += "1";
        
        fairyFlip = False;
        if self.direction == -1:
            fairyFlip = True;
            
        aGame.drawImage(IMGLIB_CHARACTER.images[fairyImg], self.gameObj.x + self.fairyOffset, self.gameObj.getShadowDrawY() - 50 + math.sin(self.fairyTime / 10) * 4, fairyFlip);        
    
    def attackControl(self):
        if self.manager.isWinCondition() and self.manager.isEmptyLevel():
            return;
        
        if self.control.a:
            self.setState(self.ST_ATTACK_PLUS);
            return True;
        elif self.control.b:
            self.setState(self.ST_ATTACK_MINUS);
            return True;
        elif self.control.c:
            self.setState(self.ST_ATTACK_DIVIDE);
            return True;
        return False;
    
    def onSetState(self):
        if self.state == self.ST_STAND:
            self.gameObj.setAnim(ANIM_CHARACTER_STAND);
            self.gameObj.friction = 0.6;
        elif self.state == self.ST_WALK:
            self.gameObj.setAnim(ANIM_CHARACTER_WALK);
            self.stopMovement();
        elif self.state == self.ST_ATTACK_PLUS:
            self.gameObj.setAnim(ANIM_CHARACTER_ATTACK_A);
            self.manager.playSound(SND_ATTACK_LAUNCH);
            self.stopMovement();
            self.turnLogic();
        elif self.state == self.ST_ATTACK_MINUS:
            self.gameObj.setAnim(ANIM_CHARACTER_ATTACK_A);
            self.manager.playSound(SND_ATTACK_LAUNCH);
            self.stopMovement();
            self.turnLogic();
        elif self.state == self.ST_ATTACK_DIVIDE:
            self.gameObj.setAnim(ANIM_CHARACTER_ATTACK_A);
            self.manager.playSound(SND_ATTACK_LAUNCH);
            self.stopMovement();
            self.turnLogic();
        elif self.state == self.ST_WIN:
            self.gameObj.setAnim(ANIM_CHARACTER_WIN);
            self.stopMovement();
        
        return;
    
    def ST_STAND(self):
        self.turnLogic();
        
        if self.attackControl():
            return;
        
        if self.control.anyDir:
            self.setState(self.ST_WALK);
            return;
        
    def ST_WALK(self):
        self.turnLogic();
        
        if self.attackControl():
            return;
        
        if not self.control.anyDir:
            self.setState(self.ST_STAND);
            return;
        
        walkSpeed = 2;
        
        if self.control.up:
            self.gameObj.translateZ(-walkSpeed);
        if self.control.down:
            self.gameObj.translateZ(walkSpeed);
        
        if self.control.left:
            self.gameObj.translateX(-walkSpeed);
        if self.control.right:
            self.gameObj.translateX(walkSpeed);
        
    def ST_ATTACK_PLUS(self):
        if self.gameObj.animEnd:
            self.setState(self.ST_STAND);
            return;
        
        if self.gameObj.newFrame and self.gameObj.frameIndex == 4:
            self.manager.spawnPlayerAttack("+");
        
        if self.stateTime > 24:
            if self.attackControl():
                return;
            
    def ST_ATTACK_MINUS(self):
        if self.gameObj.animEnd:
            self.setState(self.ST_STAND);
            return;
        
        if self.gameObj.newFrame and self.gameObj.frameIndex == 4:
            self.manager.spawnPlayerAttack("-");
        
        if self.stateTime > 24:
            if self.attackControl():
                return;
            
    def ST_ATTACK_DIVIDE(self):
        if self.gameObj.animEnd:
            self.setState(self.ST_STAND);
            return;
        
        if self.gameObj.newFrame and self.gameObj.frameIndex == 4:
            self.manager.spawnPlayerAttack("/");
        
        if self.stateTime > 24:
            if self.attackControl():
                return;
            
    def ST_WIN(self):
        if self.gameObj.animEnd:
            self.readyToNextLevel = True;
    
class Ghost(GameCharacter):
    def __init__(self, aX, aZ, aDirection, aManager, aLife, aDropValue = 3):
        self.life = aLife;
        GameCharacter.__init__(self, aX, 0, aZ, aDirection, None, IMGLIB_GHOST, aManager);
        self.floatingValue = 0.0;
        self.showNumber = True;
        self.setState(self.ST_APPEARING);
        self.dead = False;
        self.gameObj.y = -8;
        self.gameObj.gravity = 0;
        self.destinationPos = (0,0);
        self.waitFrames = 0;
        self.pairRender = False;
        self.doublePairRender = False;
        self.dropValue = aDropValue;
        self.showValue = self.life;
        self.pairUpdate = False;
        self.doublePairUpdate = False;
        
    def update(self):
        GameCharacter.update(self);
        
        self.pairUpdate = not self.pairUpdate;
        if self.pairUpdate:
            self.doublePairUpdate = not self.doublePairUpdate;
        
        if self.doublePairUpdate:
            if self.showValue > self.life:
                if self.showValue - 10 > self.life:
                    self.showValue -= 5;
                else:
                    self.showValue -= 1;
                if self.showValue < self.life:
                    self.showValue = self.life;
            elif self.showValue < self.life:
                if self.showValue + 10 < self.life:
                    self.showValue += 5;
                else:
                    self.showValue += 1;
                if self.showValue > self.life:
                    self.showValue = self.life;

    def onSetState(self):

        self.gameObj.friction = 0;
        self.gameObj.boundX = -0.8;
        self.gameObj.boundY = -0.75;
        
        if self.gameObj.velY < 0.0:
            self.gameObj.velY = 0.0;
            
        if self.life < 0:
            self.imgLib = IMGLIB_GHOST_NEGATIVE;
        elif self.life > 0:
            self.imgLib = IMGLIB_GHOST;

        self.showNumber = True;
        
        if self.state == self.ST_APPEARING:
            self.gameObj.setAnim(ANIM_GHOST_APPEARING);
            self.showNumber = False;
        elif self.state == self.ST_WAIT:
            self.gameObj.setAnim(ANIM_GHOST_NORMAL);
            self.waitFrames = random.randint(60,240);
            self.gameObj.velX = 0.0;
            self.gameObj.velZ = 0.0;
        elif self.state == self.ST_MOVE_TO_DESTINATION:
            self.gameObj.setAnim(ANIM_GHOST_NORMAL);
            self.chooseDestinationPos();
            self.lookToDestination();
            self.gameObj.velX = 0.0;
            self.gameObj.velZ = 0.0;
        elif self.state == self.ST_DAMAGE:
            self.gameObj.setAnim(ANIM_GHOST_DAMAGE);
            self.gameObj.velX = 2.0 * -self.direction;
            self.gameObj.friction = 0.03;
            self.gameObj.gravity = 0.025;
            self.gameObj.velY = -0.5;
            self.gameObj.pauseTime = 8;
            self.shakeTime = 2;
            self.manager.playSound(SND_GHOST_DAMAGE);
        elif self.state == self.ST_RESTORATION:
            self.gameObj.setAnim(ANIM_GHOST_LAUGH);
            self.gameObj.velX = 1.0 * -self.direction;
            self.gameObj.friction = 0.03;
            self.gameObj.gravity = 0.025;
            self.gameObj.velY = -0.5;
            self.gameObj.pauseTime = 4;
            self.shakeTime = 2;
            self.manager.playSound(SND_GHOST_LAUGH);
        elif self.state == self.ST_DEAD:
            self.gameObj.setAnim(ANIM_GHOST_DEAD);
            self.gameObj.velX = 0.0;
            self.gameObj.gravity = -0.04;
            self.gameObj.velY = 0.0;
            self.gameObj.pauseTime = 30;
            self.shakeTime = 30;
            self.manager.playSound(SND_GHOST_DAMAGE);
            self.manager.playSound(SND_GHOST_DEAD);
            i = 0;
            while i < self.dropValue:
                self.manager.spawnDiamond(self.gameObj.x, self.gameObj.y, self.gameObj.z);
                i += 1;
            
    
    def render(self, aGame):
        
        self.pairRender = not self.pairRender;
        if self.pairRender:
            self.doublePairRender = not self.doublePairRender;
        
        if self.direction == -1:
            mirror = True;
        else:
            mirror = False;
            
        if self.state != self.ST_APPEARING and self.state != self.ST_DEAD:
            aGame.drawImage(self.imgLib.images["shadow"], self.gameObj.x, WALL_POS + self.gameObj.z * 0.5, mirror);
        
        offset = 0;
        if self.shakeTime > 0 and self.doublePairRender:
            offset = 1;
        

        aGame.drawImage(self.imgLib.images[self.gameObj.currentFrame], self.gameObj.x + offset * self.direction, self.getDrawY() + math.sin(self.floatingValue) * 4, mirror, (pygame.BLEND_ADD));

        numOffsetX = (FNT_CLEARLY.charSize[0] * len(str(self.life))) / 2;
        numOffsetX += 1;
        numOffsetX -= 3 * self.direction;

        if self.showNumber:#draw number
            aGame.drawText(FNT_CLEARLY, self.gameObj.x - numOffsetX, WALL_POS + self.gameObj.z * 0.5 + self.gameObj.y + math.sin(self.floatingValue) * 4 - 16, str(self.showValue));
    
    def ST_MOVE_TO_DESTINATION(self):
        self.updateAttackContact();
        if self.stateTime == 0:
            return;
        self.moveToDestinationPos(0.5);
        self.updateFloatingValue();
        self.updateFloatingValue();
        self.updateFloatingValue();
        if self.gameObj.x == self.destinationPos[0] and self.gameObj.z == self.destinationPos[1]:
            self.setState(self.ST_WAIT);
    
    def ST_WAIT(self):
        self.updateAttackContact();
        if self.stateTime == 0:
            return;
        
        self.updateFloatingValue();
        self.lookMainCharacter();
        self.waitFrames -= 1;
        if self.waitFrames <= 0:
            self.setState(self.ST_MOVE_TO_DESTINATION);
            return;
    
    def ST_DAMAGE(self):
        
        self.updateAttackContact();
        if self.stateTime == 0:
            return;
        
        if self.stateTime > 60:
            self.setState(self.ST_WAIT);
            return;
    
    def ST_RESTORATION(self):
        self.updateAttackContact();
        if self.stateTime == 0:
            return;
        
        if self.stateTime > 60:
            self.setState(self.ST_WAIT);
            return;
    
    def ST_APPEARING(self):
        if self.gameObj.animEnd:
            self.setState(self.ST_WAIT);
            return;
    
    def ST_DEAD(self):
        if self.gameObj.animEnd:
            self.dead = True;
        if self.gameObj.currentFrame != "damage00":
            self.showNumber = False;
    
    def isDead(self):
        return self.dead;
    
    def updateFloatingValue(self):
        self.floatingValue += 0.05;
        if self.gameObj.y > -8:
            self.gameObj.y -= 1;
            self.gameObj.gravity = 0.0;
            self.gameObj.velY = 0.0;
            if self.gameObj.y < -8:
                self.gameObj.y = -8;
                
        
    def chooseDestinationPos(self):
        self.destinationPos = (random.randint(GAME_LIMIT_LEFT + 8, GAME_LIMIT_RIGHT - 8), random.randint(GAME_LIMIT_BACK + 8, GAME_LIMIT_FRONT - 8));
        
    def moveToDestinationPos(self, aVel):
        if abs(self.gameObj.x - self.destinationPos[0]) < aVel:
            self.gameObj.x = self.destinationPos[0];
        else:
            if self.gameObj.x < self.destinationPos[0]:
                self.gameObj.translateX(aVel);
            else:
                self.gameObj.translateX(-aVel);
                
        if abs(self.gameObj.z - self.destinationPos[1]) < aVel:
            self.gameObj.z = self.destinationPos[1];
        else:
            if self.gameObj.z < self.destinationPos[1]:
                self.gameObj.translateZ(aVel);
            else:
                self.gameObj.translateZ(-aVel);
        
    def lookMainCharacter(self):
        if self.manager.mainCharacter.gameObj.x > self.gameObj.x:
            self.direction = 1;
        else:
            self.direction = -1;
            
    def lookToDestination(self):
        if self.destinationPos[0] > self.gameObj.x:
            self.direction = 1;
        else:
            self.direction = -1;
            
    def updateAttackContact(self):
        if self.gameObj.y > -24:
            if self.manager.attack != None:
                if self.manager.attack.isActive():
                    if abs(self.manager.attack.gameObj.z - self.gameObj.z) < 16:
                        if abs(self.manager.attack.gameObj.x - self.gameObj.x) < 16:
                            self.direction = -self.manager.attack.direction;
                            self.applyDamage(self.manager.attack);
                    
    def applyDamage(self, aAttack):
        
        numOffsY = 32;
        numVel = 4;
        numVelMul = 0.75;
        numWait = 12;
        
        prevLife = self.life;
        if aAttack.operator == "+":
            self.manager.spawnHudEffect(FloatString(str(self.life) + "+" + str(aAttack.number) + "=" + str(self.life + aAttack.number), self.gameObj.x, self.gameObj.getDrawY() - numOffsY, -numVel, numVelMul, numWait));
            self.life += aAttack.number;
        elif aAttack.operator == "-":
            self.manager.spawnHudEffect(FloatString(str(self.life) + "-" + str(aAttack.number) + "=" + str(self.life - aAttack.number), self.gameObj.x, self.gameObj.getDrawY() - numOffsY, -numVel, numVelMul, numWait));
            self.life -= aAttack.number;
        else:
            if prevLife == 1 or prevLife == -1:
                self.setState(self.ST_RESTORATION);
                aAttack.invalidate();
                self.manager.spawnHudEffect(FloatString( "&" + str(self.life) + "%" + str(aAttack.number) + "?", self.gameObj.x, self.gameObj.getDrawY() - numOffsY, -numVel, numVelMul, numWait));
                return;
            else:
                self.life = int(self.life / aAttack.number);
                
                if prevLife % aAttack.number != 0:
                    if math.fmod(prevLife,aAttack.number) < 0:
                        negative = True;
                        restStr = " Y SOBRA -1";
                    else:
                        negative = False;
                        restStr = " Y SOBRA 1";
                        
                    
                    self.manager.spawnHudEffect(FloatString(str(prevLife) + "%" + str(aAttack.number) + "=" + str(self.life) + restStr, self.gameObj.x, self.gameObj.getDrawY() - numOffsY, -numVel, numVelMul, numWait * 4));
                    self.manager.spawnNumberOne(self.gameObj.x, self.gameObj.z - 4, self.direction, negative);
                    self.setState(self.ST_RESTORATION);
                    aAttack.invalidate();
                    return;
                else:
                    self.manager.spawnHudEffect(FloatString(str(prevLife) + "%" + str(aAttack.number) + "=" + str(self.life), self.gameObj.x, self.gameObj.getDrawY() - numOffsY, -numVel, numVelMul, numWait));
                    
        
        if self.life == 0:
            self.setState(self.ST_DEAD);
        else:
            if abs(self.life) > abs(prevLife) and abs(self.life) > 20:
                self.setState(self.ST_RESTORATION);
            else: 
                self.setState(self.ST_DAMAGE);
            
        aAttack.invalidate();
            
class NumberOne(GameCharacter):
    def __init__(self, aX, aZ, aDirection, aNegative, aManager):
        
        if aNegative:
            imgLib = IMGLIB_NUMBER_ONE_NEGATIVE;
        else:
            imgLib = IMGLIB_NUMBER_ONE;
        
        GameCharacter.__init__(self, aX, 0, aZ, aDirection, None, imgLib, aManager);
        
        self.destX = aX;
        self.destZ = aZ;
        
        self.gameObj.friction = 0.1;
        self.gameObj.boundX = -0.2;
        self.gameObj.boundZ = -0.5;
        
        self.waitTime = 0;
        
        self.totalTime = 0;
        
        self.pairRender = False;
        self.doublePairRender = False;
        
        self.dead = False;
        self.setState(self.ST_APPEARING);
        
    def update(self):
        GameCharacter.update(self);
        self.totalTime += 1;
        
    def render(self, aGame):
        
        self.pairRender = not self.pairRender;
        if self.pairRender:
            self.doublePairRender = not self.doublePairRender;
        
        if self.direction == -1:
            sufix = "l";
        else:
            sufix = "r";
            
        offset = 0;
        if self.gameObj.pauseTime > 0 and self.doublePairRender:
            offset = -1;
        
        aGame.drawImage(self.imgLib.images[self.gameObj.currentFrame + sufix], self.gameObj.x + offset * self.direction, self.getDrawY(), False);
        
    def onSetState(self):
        
        if self.state == self.ST_APPEARING:
            self.gameObj.setAnim(ANIM_NUMBER_ONE_APPEARING);
        elif self.state == self.ST_IDLE:
            self.gameObj.setAnim(choice((ANIM_NUMBER_ONE_IDLE_A, ANIM_NUMBER_ONE_IDLE_B)));
            self.waitTime = random.randint(30, 120);
        elif self.state == self.ST_DEADING:
            self.gameObj.setAnim(ANIM_NUMBER_ONE_DEADING);
        elif self.state == self.ST_WALKING:
            self.gameObj.setAnim(ANIM_NUMBER_ONE_WALKING);
            self.chooseDestination();
            if self.destX < self.gameObj.x:
                self.direction = -1;
            else:
                self.direction = 1;
        elif self.state == self.ST_STEALING:
            self.gameObj.setAnim(ANIM_NUMBER_ONE_STEALING);
        elif self.state == self.ST_DAMAGE:
            self.gameObj.setAnim(ANIM_NUMBER_ONE_DAMAGE);
            self.gameObj.pauseTime = 8;
            self.gameObj.velX = -4 * self.direction;
            self.gameObj.velZ = -2;
            self.manager.playSound(SND_NUMBER_ONE_DAMAGE);
        
    def ST_APPEARING(self):
        if self.gameObj.animEnd:
            self.setState(self.ST_IDLE);
            return;
    
    def ST_DEADING(self):
        if self.gameObj.animEnd:
            self.dead = True;
            return;
    
    def ST_IDLE(self):
        if self.updateAttackContact():
            return;
        self.waitTime -= 1;
        if self.waitTime < 0:
            self.waitTime = 0;
            
            if self.totalTime > 60 * 20:
                self.setState(self.ST_DEADING);
            else:
                self.setState(self.ST_WALKING);
            return;
        
    def ST_WALKING(self):
        if self.updateAttackContact():
            return;
        self.moveToDestinationPos(2);
        if self.manager.tryStealDiamond(self.gameObj.x, self.gameObj.z):
            self.setState(self.ST_STEALING);
            return;
        
        if self.gameObj.x == self.destX and self.gameObj.z == self.destZ:
            self.setState(self.ST_IDLE);
            return;
        
    def ST_STEALING(self):
        if self.updateAttackContact():
            return;
        if self.gameObj.animEnd:
            self.setState(self.ST_IDLE);
            return;
        
    def ST_DAMAGE(self):
        if self.updateAttackContact():
            return;
        
        if self.stateTime > 30 and abs(self.gameObj.velX) < 0.1:
            self.setState(self.ST_IDLE);
            return;
    
    def moveToDestinationPos(self, aVel):
        if abs(self.gameObj.x - self.destX) < aVel:
            self.gameObj.x = self.destX;
        else:
            if self.gameObj.x < self.destX:
                self.gameObj.translateX(aVel);
            else:
                self.gameObj.translateX(-aVel);
                
        if abs(self.gameObj.z - self.destZ) < aVel:
            self.gameObj.z = self.destZ;
        else:
            if self.gameObj.z < self.destZ:
                self.gameObj.translateZ(aVel);
            else:
                self.gameObj.translateZ(-aVel);
    
    def chooseDestination(self):
        
        diamondPos = self.manager.getStillDiamondPos();
        if diamondPos == None:
            self.chooseRandomDestination();
            return;
        else:
            self.destX = diamondPos[0];
            self.destZ = diamondPos[1];
            
    def chooseRandomDestination(self):
        self.destX = random.randint(GAME_LIMIT_LEFT + 4, GAME_LIMIT_RIGHT - 4);
        self.destZ = random.randint(GAME_LIMIT_BACK + 4, GAME_LIMIT_FRONT - 4);
        
    def updateAttackContact(self):
        if self.manager.attack != None:
            if self.manager.attack.isActive():
                if abs(self.manager.attack.gameObj.z - self.gameObj.z) < 16:
                    if abs(self.manager.attack.gameObj.x - self.gameObj.x) < 12:
                        self.direction = -self.manager.attack.direction;
                        self.setState(self.ST_DAMAGE);
                        self.manager.attack.invalidate();
                        return True;
        return False;
    
class Attack:
    def __init__(self, aX, aZ, aDirection, aNumber, aOperator, aManager):
        self.gameObj = GameObject();
        self.gameObj.x = aX;
        self.gameObj.z = aZ;
        self.gameObj.velX = aDirection * 4;
        self.gameObj.friction = 0.1;
        self.gameObj.y = -16;
        self.gameObj.gravity = 0.0;
        self.number = aNumber;
        self.graphicNumber = str(aNumber);
        self.lifeTime = 40;
        self.pairRender = False;
        self.active = True;
        self.direction = aDirection;
        self.manager = aManager;
        
        self.operator = aOperator;
        self.graphic = "";
        self.allowMirror = False;
        if aOperator == "+":
            self.graphic = "plus";
            self.allowMirror = True;
        elif aOperator == "-":
            self.graphic = "minus";
            self.allowMirror = True;
        elif aOperator == "/":
            self.graphic = "divide";
            self.allowMirror = False;
            
        self.mirrored = False;
        if self.allowMirror:
            if aDirection == -1:
                self.mirrored = True;
        else:
            if aDirection == 1:
                self.graphic += "_right";
            else:
                self.graphic += "_left";
            
        
    def update(self):
        self.gameObj.update();
        self.lifeTime -= 1;
        
    def render(self, aGame):
        self.pairRender = not self.pairRender;
        if self.lifeTime >= 20 or (self.lifeTime < 20 and self.lifeTime > 0 and self.pairRender ):
            aGame.drawImage(IMGLIB_ATTACKS.images[self.graphic], self.gameObj.x - 10, WALL_POS + self.gameObj.z * 0.5 + self.gameObj.y, self.mirrored);
            aGame.drawImage(IMGLIB_ATTACKS.images[self.graphicNumber], self.gameObj.x + 10, WALL_POS + self.gameObj.z * 0.5 + self.gameObj.y, False);

    def getDepth(self):
        return self.gameObj.z + 16;
    
    def isActive(self):
        if self.lifeTime > 8 and self.active:
            return True;
        else:
            return False;
        
    def invalidate(self):
        if self.active:
            self.active = False;
            if self.lifeTime > 20:
                self.lifeTime = 20;
            self.gameObj.velX = 0;
            self.manager.spawnEffect(SimpleAnimEffect(ANIM_SPARK, self.gameObj.x, self.gameObj.y, self.gameObj.z, choice((True,False)), (pygame.BLEND_ADD)));
        
class Diamond():
    def __init__(self, aX, aY, aZ, aManager):
        self.gameObj = GameObject();
        self.gameObj.setAnim(ANIM_DIAMOND);
        self.gameObj.x = aX;
        self.gameObj.y = aY;
        self.gameObj.z = aZ;
        self.gameObj.velX = random.uniform(-3.0,3.0);
        self.gameObj.velY = random.uniform(-5.0,-3.0);
        self.gameObj.velZ = random.uniform(-1.0,1.0);
        self.gameObj.boundX = -1.0;
        self.gameObj.boundY = -0.75;
        self.gameObj.boundZ = -1.0;
        self.gameObj.friction = 0.0;
        self.gameObj.gravity = 0.1;
        
        self.manager = aManager;
        self.dead = False;
        
        self.lifeTime = 60 * 10;
        self.pairRender = False;
        self.doublePairRender = False;
        
        self.takeable = False;
        
    def update(self):
        self.gameObj.update();
        
        if self.gameObj.velY > 0:
            self.takeable = True;
        
        if self.gameObj.boundNowY:
            self.gameObj.velX *= 0.5;
            self.gameObj.velZ *= 0.5;
            if abs(self.gameObj.velY) > 0.2:
                self.manager.playSound(SND_DIAMOND_BOUNCE);
            
            
        if abs(self.gameObj.velY) < self.gameObj.gravity * 3 and self.gameObj.y > -2:
            self.lifeTime -= 1;
            if self.lifeTime < 0:
                self.lifeTime = 0;
                self.dead = True;
            
        
    def render(self, aGame):
        
        self.pairRender = not self.pairRender;
        if self.pairRender:
            self.doublePairRender = not self.doublePairRender;
        
        if self.lifeTime < 60 * 2 and self.doublePairRender:
            return;
        
        aGame.drawImage(IMGLIB_EFFECTS.images["diamond_shadow"], self.gameObj.x, self.gameObj.getShadowDrawY(), False);
        aGame.drawImage(IMGLIB_EFFECTS.images[self.gameObj.currentFrame], self.gameObj.x, self.gameObj.getDrawY(), False);
        pass;
    
    def take(self, aByPlayer):
        if self.dead or not self.takeable:
            return;
        
        self.dead = True;
        
        self.manager.spawnEffect(SimpleAnimEffect(ANIM_SPARK, self.gameObj.x, self.gameObj.y, self.gameObj.z, choice((True,False)), (pygame.BLEND_ADD)));
        
        if aByPlayer:
            self.manager.getDiamond(self.gameObj.x, self.gameObj.getDrawY());
            self.manager.playSound(SND_DIAMOND_GET);
            self.manager.spawnHudEffect(FloatString("+1 DIAMONND", self.gameObj.x, self.gameObj.getShadowDrawY() - 32, -4, 0.75, 12));
            
    def getDepth(self):
        return self.gameObj.z;
        
class HudDiamond():
    def __init__(self, aDestX, aDestY, aInitialUpdates):
        self.active = False;
        self.moving = False;
        self.destX = aDestX;
        self.destY = aDestY;
        self.x = -1;
        self.y = -1;
        self.fromX = -1;
        self.fromY = -1;
        self.interpValue = 0.0;
        self.interpStep = 0.0;
        self.toDestination = True;
        self.originalDestinationX = aDestX;
        self.originalDestinationY = aDestY;
        self.gameObj = GameObject();
        self.gameObj.setAnim(ANIM_HUD_DIAMOND);
        
        i = 0;
        while i < aInitialUpdates:
            self.gameObj.update();
            i += 1;
        
    def update(self):
        
        self.gameObj.update();
        
        self.interpValue += self.interpStep;
        if self.interpValue >= 1.0:
            self.interpValue = 0.0;
            self.moving = False;
            if self.toDestination:
                self.fromX = self.destX;
                self.fromY = self.destY;
                self.x = self.destX;
                self.y = self.destY;
            else:
                self.active = False;
                self.fromX = -1;
                self.fromY = -1;
                self.x = -1;
                self.y = -1;
        else:
            coord = self.getCurrentCoord();
            self.x = coord[0];
            self.y = coord[1];
        
        return;
    
    def render(self, aGame):
        if self.active:
            aGame.drawImage(IMGLIB_EFFECTS.images[self.gameObj.currentFrame], self.x, self.y, False);
    
    def moveToDestination(self, aFromX, aFromY, aFrames):
        self.toDestination = True;
        self.active = True;
        
        if self.moving:
            self.putCurrentCoord();
        else:
            self.fromX = aFromX;
            self.fromY = aFromY;
            self.x = self.fromX;
            self.y = self.fromY;
            
        self.moving = True;
        self.destX = self.originalDestinationX;
        self.destY = self.originalDestinationY;
        self.interpValue = 0.0;
        self.interpStep = 1.0 / aFrames;
        
        pass;
    
    def leftFromCurrent(self, aToX, aToY, aFrames):
        if not self.active:
            return;
        self.toDestination = False;
        self.putCurrentCoord();
        self.destX = aToX;
        self.destY = aToY;
        self.interpValue = 0.0;
        self.interpStep = 1.0 / aFrames;
        self.moving = True;
    
    def getCurrentCoord(self):
        interpValue = self.interpValue;
        interpValue = 1.0 -interpValue;
        interpValue = interpValue * interpValue * interpValue * interpValue * interpValue;
        interpValue = 1.0 -interpValue;

        x = int(self.fromX + (self.destX - self.fromX) * interpValue);
        y = int(self.fromY + (self.destY - self.fromY) * interpValue);
        return (x,y);
    
    def putCurrentCoord(self):
        p = self.getCurrentCoord();
        self.fromX = p[0];
        self.fromY = p[1];
        self.x = self.fromX;
        self.y = self.fromY;
        
class FloatString:
    def __init__(self, aText, aX, aY, aVelY, aVelMultiplier, aWaitTime, aFixX = True):
        self.text = aText;
        self.x = aX;
        self.y = aY;
        
        strWidth = (FNT_CLEARLY.charSize[0] * len(aText));
        
        if aFixX:
            self.x -= strWidth/2;
            
            if self.x < 8:
                self.x = 8;
            elif self.x + strWidth > 300 - 8:
                self.x = 300 - 8 - strWidth;
        
        self.velY = aVelY;
        self.velMultiplier = aVelMultiplier;
        
        self.lifeTime = aWaitTime;
        self.dead = False;
        
    def update(self):
        self.y += self.velY;
        self.velY *= self.velMultiplier;
        if abs(self.velY) < 0.01:      
            self.velY = 0;  
            self.lifeTime -= 1;
            if self.lifeTime < 0:
                self.dead = True;
    
    def render(self, aGame):
        aGame.drawText(FNT_CLEARLY, self.x, self.y, self.text);
        pass;
        

class NozarTimeUpEffect:
    def __init__(self, aManager):
        self.dead = False;
        self.manager = aManager;
        self.interpValue = 0.0;
        self.interpVel = 1.0 / 60;
        self.sequence = 0;
        self.time = 0;
        
        self.SEQUENCE_ENTER = 0;
        self.SEQUENCE_ABSORB_DIAMONDS = 1;
        self.SEQUENCE_WAIT_DIAMONDS = 2;
        self.SEQUENCE_LAUGH = 3;
        self.SEQUENCE_LEAVE = 4;
        
        self.manager.playSound(SND_NOZAR_APPEAR);
    
    def update(self):
        self.time += 1;
        
        self.interpValue += self.interpVel;
        if self.interpValue > 1.0:
            self.interpValue = 1.0;
            if self.sequence == self.SEQUENCE_ENTER:
                self.sequence = self.SEQUENCE_ABSORB_DIAMONDS;
            elif self.sequence == self.SEQUENCE_LEAVE:
                self.dead = True;
                return;
                
                
        if self.sequence == self.SEQUENCE_ABSORB_DIAMONDS and self.time % 8 == 0:
            if self.time % 16 == 0:
                x = 80;
            else:
                x = 300 - 80;
                
            self.manager.playSound(SND_ATTACK_LAUNCH);
            mustStop = not self.manager.leftDiamond(x, 75, 60);
            
            if mustStop:
                self.time = 0;
                self.sequence = self.SEQUENCE_WAIT_DIAMONDS;
                
                
            return;
        
        if self.sequence == self.SEQUENCE_WAIT_DIAMONDS:
            if self.time > 60:
                self.time = 0;
                self.sequence = self.SEQUENCE_LAUGH;
                self.manager.playSound(SND_GHOST_LAUGH);
        
        if self.sequence == self.SEQUENCE_LAUGH:
            if self.time > 120:
                self.sequence = self.SEQUENCE_LEAVE;
                self.interpValue = 0.0;
                return;
            
        
            
        
    
    def render(self, aGame):
        if self.sequence != self.SEQUENCE_LEAVE:
            interpValue = 1.0 - self.interpValue * self.interpValue;
        else:
            interpValue = self.interpValue * self.interpValue;
            
        laughOffset = 0;
        if self.sequence == self.SEQUENCE_LAUGH and self.time % 16 < 8:
            laughOffset = 2;
        
        aGame.drawImage(IMGLIB_EFFECTS.images["nozar_face"], 300 / 2, 60 - 90 * interpValue + laughOffset, False);
        aGame.drawImage(IMGLIB_EFFECTS.images["nozar_hand"], 80 - 90 * interpValue, 70 - 90 * interpValue, False);
        aGame.drawImage(IMGLIB_EFFECTS.images["nozar_hand"], 300 - 80 + 90 * interpValue, 70 - 90 * interpValue, True);


class SimpleAnimEffect:
    def __init__(self, aAnim, aX, aY, aZ, aMirror, aDrawParams = 0 , aVelX = 0, aVelY = 0, aVelZ = 0, aGravity = 0):
        self.gameObj = GameObject();
        self.gameObj.x = aX;
        self.gameObj.y = aY;
        self.gameObj.z = aZ;
        self.gameObj.velX = aVelX;
        self.gameObj.velY = aVelY;
        self.gameObj.velZ = aVelZ;
        self.gameObj.setAnim(aAnim);
        self.mirror = aMirror;
        self.drawParams = aDrawParams;
        self.dead = False;
        self.gameObj.gravity = aGravity;
        self.gameObj.setAnim(aAnim);
    
    def update(self):
        self.gameObj.update();
        
        if self.gameObj.animEnd:
            self.dead = True;
        
        
    def render(self, aGame):
        aGame.drawImage(IMGLIB_EFFECTS.images[self.gameObj.currentFrame], self.gameObj.x, self.gameObj.getDrawY(), self.mirror, self.drawParams);
    
    def getDepth(self):
        return self.gameObj.z;


'''
    GAMEPLAY CLASSES
''' 
        
class GameObject:
    
    
    def __init__(self):
        self.x = 0.0;
        self.y = 0.0;
        self.z = 0.0;
        self.velX = 0.0;
        self.velY = 0.0;
        self.velZ = 0.0;
        self.velLimitX = 9999.9;
        self.velLimitY = 9999.9;
        self.velLimitZ = 9999.9;
        
        self.boundX = 0.0;
        self.boundY = 0.0;
        self.boundZ = 0.0;
        self.gravity = 0.2;
        self.friction = 1.0;
        
        self.boundNowX = False;
        self.boundNowY = False;
        self.boundNowZ = False;
        
        self.anim = [];
        self.frameIndex = -1;
        self.frameTime = 0;
        self.frameDuration = 4;
        self.loopIndex = -1;
        self.currentFrame = None;
        self.animEnd = False;
        self.newFrame = False;
        
        self.pauseTime = 0;
        self.freezeTime = 0;
        
    
    def update(self):
        
        self.boundNowX = False;
        self.boundNowY = False;
        self.boundNowZ = False;
        
        self.newFrame = False;
        
        if self.pauseTime > 0:
            self.pauseTime -= 1;
        else:
            if self.freezeTime > 0:
                self.freezeTime -= 1;
            else:
                #UPDATE PHYSIC
                self.velY += self.gravity;
                
                if self.velX > self.velLimitX:
                    self.velX = self.velLimitX;
                elif self.velX < -self.velLimitX:
                    self.velX = -self.velLimitX;
                elif abs(self.velX) > self.friction:
                    self.velX -= self.friction * sign(self.velX);
                else:
                    self.velX = 0;
                    
                if self.velY > self.velLimitY:
                    self.velY = self.velLimitY;
                elif self.velY < -self.velLimitY:
                    self.velY = -self.velLimitY;
                    
                if self.velZ > self.velLimitZ:
                    self.velZ = self.velLimitZ;
                elif self.velZ < -self.velLimitZ:
                    self.velZ = -self.velLimitZ;
                elif abs(self.velZ) > self.friction:
                    self.velZ -= self.friction * sign(self.velZ);
                else:
                    self.velZ = 0;
                
                self.x += self.velX;
                if self.x > GAME_LIMIT_RIGHT:
                    self.x = GAME_LIMIT_RIGHT;
                    if self.velX > 0.0:
                        self.velX = self.velX * self.boundX;
                        self.boundNowX = True;
                elif self.x < GAME_LIMIT_LEFT:
                    self.x = GAME_LIMIT_LEFT;
                    if self.velX < 0.0:
                        self.velX = self.velX * self.boundX;
                        self.boundNowX = True;
                
                self.y += self.velY;
                if self.y > 0.0:
                    self.y = 0;
                    if self.velY > 0:
                        self.velY = self.velY * self.boundY;
                        self.boundNowY = True;
                
                self.z += self.velZ;
                if self.z > GAME_LIMIT_FRONT:
                    self.z = GAME_LIMIT_FRONT;
                    if self.velZ > 0.0:
                        self.velZ = self.velZ * self.boundZ;
                        self.boundNowZ = True;
                elif self.z < GAME_LIMIT_BACK:
                    self.z = GAME_LIMIT_BACK;
                    if self.velZ < 0.0:
                        self.velZ = self.velZ * self.boundZ;
                        self.boundNowZ = True;
            
            #UPDATE ANIMATION
            if len(self.anim) > 0:
                self.frameTime = self.frameTime - 1;
                if self.frameTime < 0:
                    self.advanceFrame();
                
    def applyForce(self, aForceX, aForceY, aForceZ):
        self.velX += aForceX;
        self.velY += aForceY;
        self.velZ += aForceZ;
        
    def translateX(self, aX):
        self.x += aX;
        if self.x > GAME_LIMIT_RIGHT:
            self.x = GAME_LIMIT_RIGHT;
        elif self.x < GAME_LIMIT_LEFT:
            self.x = GAME_LIMIT_LEFT;
            
    def translateY(self, aY):
        self.y += aY;
        if self.y > 0:
            self.y = 0;
            
    def translateZ(self, aZ):
        self.z += aZ;
        if self.z > GAME_LIMIT_FRONT:
            self.z = GAME_LIMIT_FRONT;
        elif self.z < GAME_LIMIT_BACK:
            self.z = GAME_LIMIT_BACK;
        
    
    def advanceFrame(self):
        self.frameTime = self.frameDuration;
        self.frameIndex = self.frameIndex + 1;
        self.newFrame = True;
        if self.frameIndex >= len(self.anim):
            if self.loopIndex == -1:
                self.frameIndex = self.frameIndex - 1;
                self.animEnd = True;
                self.newFrame = False;
            else:
                self.frameIndex = self.loopIndex;
        self.currentFrame = self.anim[self.frameIndex];
        
    def setAnim(self, aAnim):
        self.anim = aAnim.frames;
        self.loopIndex = aAnim.loopIndex;
        self.frameDuration = aAnim.frameDuration;
        self.frameIndex = 0;
        self.frameTime = self.frameDuration;
        self.animEnd = False;
        self.currentFrame = self.anim[0];
        self.newFrame = True;
        
    def getDrawY(self):
        return WALL_POS + self.z * 0.5 + self.y;
    
    def getShadowDrawY(self):
        return WALL_POS + self.z * 0.5;
        
'''
    TEST CLASSES
'''        
class TestObj:
    def __init__(self):
        self.gameObject = GameObject();
        self.gameObject.setAnim(ANIM_CHARACTER_STAND);
        self.updtF = self.updateFunc;
    
    def update(self):
        self.updtF();
    
    def updateFunc(self):
        self.gameObject.update();        
        
    def render(self, aGame):
        aGame.drawImage(IMGLIB_CHARACTER.images[self.gameObject.currentFrame], 100, 100, False);
        
        
        
        
        
        