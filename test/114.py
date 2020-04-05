# -*- coding: utf-8 -*-
'''
Created on Oct 14, 2012

@author: SebaGames
'''

import pygame;
from xml.dom.minidom import parseString;

class Game:
    
    def __init__(self):
        self.time = 0.0;
        self.bmpCollection = dict();
        self.screen = None;
        self.bgBmp = None;
        self.mustRefreshBg = False;
        self.drawInstructions = list();
        self.drawInstructionCount = 0;
        self.gameState = None;
        self.scale = 1;
        self.scaleFilter = False;
        self.nextState = None;
        self.soundsToPlay = list();
        self.mute = False;
    
    def init(self, aGameState, aScreen, aScale = 1, aScaleFilter = False, aMute = False):
        self.time = 0.0;
        self.screen = aScreen;
        self.scale = aScale;
        self.scaleFilter = aScaleFilter;
        self.nextState = aGameState;
        self.mute = aMute;

        repeat = 0;
        while(repeat < 1024):
            self.drawInstructions.append(DrawInstruction());
            repeat += 1;    
            
        self.lastDrawInstructionCount = 0;    
        
        #TEST
        #self.g = self.loadImageLib("assets/win_portraits.xml");
        #self.setBackground("assets/bg.png");
        #self.sf = SpriteFont();
        #self.sf.compose(self.loadBitmap("assets/baloon_gold.png"), (9,9), (-2,4), " !'ABCDEFGHIJKLMNOPQRSTUVWXYZ%()@+,-./0123456789:");
        
    def destroy(self):
        for bmp in self.bmpCollection:
            del bmp;
            
    def update(self):
        self.time = self.time + 1.0/60.0;
        
        del self.soundsToPlay[0:len(self.soundsToPlay)];
        
        if self.nextState != None:
            self.gameState = self.nextState;
            self.nextState = None;
            self.gameState.init(self);
        
        
        
        if self.gameState != None:
            self.gameState.update();
            
        #play sounds here
        for sound in self.soundsToPlay:
            self._sndPlay(sound);
        
    def render(self):
        if self.mustRefreshBg and self.bgBmp != None:
            self.bgBmp.drawAsBackground(self.screen);
        else:
            for i in range(0,self.drawInstructionCount):
                self.drawInstructions[i].restoreBackground(self.bgBmp, self.screen);

        self.mustRefreshBg = False;
        self.drawInstructionCount = 0;

        #Calls gameplay render to add new drawInstructions
        #self.gameplayInstance.render(self);
        
        if self.gameState != None:
            self.gameState.render(self);
        
        #TEST
        #self.drawImage(self.g.images["secretary"], 50 + self.time * 4, 192, False, pygame.BLEND_RGB_MAX);
        #self.drawImage(self.g.images["succubus"], 150 + self.time * 4, 192, True);
        #self.drawText(self.sf, 8, 24, "TE ODIO CON TODO MI CORAZON PYTHON!#(Y NO ES JODA)");
        #self.drawText(self.sf, 50, 180, "RENDERS: " + str(self.lastDrawInstructionCount));
        
        self.lastDrawInstructionCount = self.drawInstructionCount;
        
        #draws new drawInstructions
        for i in range(0,self.drawInstructionCount):
            self.drawInstructions[i].draw(self.screen);
         
    def loadBitmap(self, aBmpPath):
        if not self.bmpCollection.has_key(aBmpPath):
            self.bmpCollection[aBmpPath] = Bitmap(pygame.image.load(aBmpPath), self.scale, self.scaleFilter);
        return self.bmpCollection[aBmpPath];
        
    def loadImageLib(self, aPath):
        imgLib = ImageLibrary();
        imgLib.compose(aPath, self);
        return imgLib;
    
    def loadFont(self, aPath, aCharSize, aCharSpacing, aCharacters):
        fnt = SpriteFont();
        fnt.compose(self.loadBitmap(aPath), aCharSize, aCharSpacing, aCharacters);
        
        return fnt;
        
    def setBackground(self, aBmpPath):
        self.bgBmp = self.loadBitmap(aBmpPath);
        self.mustRefreshBg = True;
        
    def drawFrame(self, aFrame, aX, aY, aFlipH):
        offstX = aFrame.offset[0];
        offstY = aFrame.offset[1];
        if aFlipH:
            offstX = -offstX;
        self.drawImage(aFrame.image, aX + offstX, aY + offstY, aFlipH);
        
    def drawImage(self, aImage, aX, aY, aFlipH, aFlags = 0):
        i = self.drawInstructions[self.drawInstructionCount];
        i.setValues(aX,aY,aFlipH,aImage, aFlags);
        self.drawInstructionCount += 1;
        
    def drawText(self, aFont, aX, aY, aText, aFlags = 0):
        aFont.draw(self, (aX, aY), aText, aFlags);
        
    def drawCenteredText(self, aFont, aX, aY, aText, aFlags = 0):
        assert isinstance(aFont,SpriteFont);
        
        txtWidth = len(aText) * aFont.charSize[0];
        aX -= txtWidth/2;
        if aX < 0:
            aX = 0;
        elif aX + txtWidth > 300:
            aX = 300 - txtWidth;
            
        self.drawText(aFont, aX, aY, aText, aFlags);
        
    
    def playMusic(self, aPath):
        if self.mute:
            return;
        pygame.mixer.music.stop();
        pygame.mixer.music.load(aPath);
        pygame.mixer.music.play(999999);
        pass;
    
    def stopMusic(self):
        if self.mute:
            return;
        pygame.mixer.music.stop();
        pass;
    
    def loadSound(self, aPath):
        return pygame.mixer.Sound(aPath);
    
    def playSound(self, aSound):
        if self.soundsToPlay.count(aSound) == 0:
            self.soundsToPlay.append(aSound);
            
    def _sndPlay(self, aSound):
        if self.mute:
            return;
        aSound.play();

'''
    GRAPHICS CLASSES
'''      
class Bitmap:
    def __init__(self, aBmp, aScale, aScaleFilter):
        self.bmp = aBmp;
        size = self.bmp.get_size();
        self.width = size[0];
        self.height = size[1];
        self.bmpMirror = self.bmp.copy();
        self.bmpMirror = pygame.transform.flip(self.bmpMirror, True, False);
        self.scale = aScale;
        self.scaleFilter = aScaleFilter;
        if self.scaleFilter:
            if aScale == 2:
                self.bmp = pygame.transform.scale2x(self.bmp);
                self.bmpMirror = pygame.transform.scale2x(self.bmpMirror);
            elif aScale == 4:
                self.bmp = pygame.transform.scale2x(self.bmp);
                self.bmp = pygame.transform.scale2x(self.bmp);
                self.bmpMirror = pygame.transform.scale2x(self.bmpMirror);
                self.bmpMirror = pygame.transform.scale2x(self.bmpMirror);
            else:
                self.scale = 1;
        else:
            if aScale == 2 or aScale == 3 or aScale == 4:
                self.bmp = pygame.transform.scale(self.bmp,(self.width * aScale, self.height * aScale));
                self.bmpMirror = pygame.transform.scale(self.bmpMirror,(self.width * aScale, self.height * aScale));
            else:
                self.scale = 1;
        
    def drawPart(self, aMirror, aPosX, aPosY, aAxisX, aAxisY, aSrcRectX, aSrcRectY, aSrcRectW, aSrcRectH, aScreen, aFlags = 0):
        b = None;
        if aMirror: 
            b = self.bmpMirror;
            aSrcRectX = self.width - (aSrcRectX + aSrcRectW);
            aAxisX = aSrcRectW - aAxisX;
        else: 
            b = self.bmp;
            
        aPosX -= aAxisX;
        aPosY -= aAxisY;
            
        aScreen.blit(b, (aPosX * self.scale, aPosY * self.scale), (aSrcRectX * self.scale, aSrcRectY * self.scale, aSrcRectW * self.scale, aSrcRectH * self.scale), aFlags);
        return (aPosX * self.scale,aPosY * self.scale,aSrcRectW * self.scale,aSrcRectH * self.scale);
        
    def drawAsBackground(self, aScreen):
        aScreen.blit(self.bmp,(0,0));
        
    def drawAsBackgroundPart(self, aSubRect, aScreen):
        aScreen.blit(self.bmp, aSubRect, aSubRect);
        
class Image:
    def __init__(self):
        self.srcRect = (0,0,0,0);
        self.srcBitmap = None;
        self.axis = (0.0,0.0);
    
    def draw(self, aPosX, aPosY, aFlipH, aScreen, aFlags = 0):
        return self.srcBitmap.drawPart(aFlipH, aPosX, aPosY, self.axis[0], self.axis[1], self.srcRect[0], self.srcRect[1], self.srcRect[2], self.srcRect[3], aScreen, aFlags);
    
class ImageLibrary:
    def __init__(self):
        self.images = dict();
    
    def compose(self, aXmlPath, aGame):
        f = open(aXmlPath, "r");
        xml = parseString(f.read());
        f.close();
        
        #n = xml.getElementsByTagName("LibraryInfo");
        
        for li in xml.getElementsByTagName("LibraryInfo"):
            for d in li.getElementsByTagName("data"):
                for sprData in d.getElementsByTagName("SpriteData"):
                    img = Image();
                    
                    #assign axis
                    csvValues = sprData.getAttribute("axis").split(",");
                    img.axis = (float(csvValues[0]),float(csvValues[1]));
                    
                    #assign source rectangle
                    csvValues = str(sprData.getAttribute("sourceRect")).split(",");
                    img.srcRect = (int(csvValues[0]),int(csvValues[1]),int(csvValues[2]),int(csvValues[3]));
                    
                    #assign and load bitmap
                    img.srcBitmap = aGame.loadBitmap(aXmlPath.rsplit("/",1)[0] + "/" + str(sprData.getAttribute("sourceImage")) + ".png");
                    
                    self.images[sprData.getAttribute("keyName")] = img;
    
class Frame:
    def __init__(self):
        self.image = None;
        self.offset = (0,0);

class SpriteFont:
    def __init__(self):
        self.images = dict();
        self.charSize = (0,0);
        self.imgSize = (0,0);
    
    def compose(self, aBmp, aCharSize, aCharSeparation, aCharList):
        
        self.imgSize = aCharSize;
        x = 0;
        y = 0;
        for char in aCharList:
            img = Image();
            img.srcBitmap = aBmp;
            img.axis = (0,0);
            img.srcRect = (x, y, aCharSize[0], aCharSize[1]);
            x += aCharSize[0];
            if x >= aBmp.width:
                x = 0;
                y += aCharSize[1];
            self.images[char] = img;
            
        self.charSize = (aCharSize[0] + aCharSeparation[0], aCharSize[1] + aCharSeparation[1]);
            
    def draw(self, aGame, aPos, aText, aFlags = 0):
        x = aPos[0];
        y = aPos[1];
        for char in aText:
            if self.images.has_key(char) and char != " ":
                aGame.drawImage(self.images[char], x, y, False, aFlags);
            x += self.charSize[0];
            if char == "#":
                x = aPos[0];
                y += self.charSize[1];
    
class DrawInstruction:
    def __init__(self):
        self.image = None;
        self.pos = (0,0);
        self.flipH = False;
        self.dirtyRectangle = (0,0,0,0);
        self.flags = 0;
    
    def setValues(self, aX, aY, aFlipH, aImage, aFlags = 0):
        self.image = aImage;
        self.pos = (aX,aY);
        self.flipH = aFlipH;
        self.flags = aFlags;
    def restoreBackground(self, aBgBmp, aScreen):
        if aBgBmp != None:
            aBgBmp.drawAsBackgroundPart(self.dirtyRectangle, aScreen);
    def draw(self, aScreen):
        self.dirtyRectangle = self.image.draw(self.pos[0], self.pos[1], self.flipH, aScreen, self.flags);

