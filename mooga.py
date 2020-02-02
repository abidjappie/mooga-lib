""" Mooga Library provides a simplified interface for 2D game development in Python. """
import pygame
import time
import os

class Color:
    """ A library of colors in (R, G, B) format from imgonline. """
    black = 0, 0, 0
    grey = 128, 128, 128
    white_smoke = 245, 245, 245
    white = 255, 255, 255
    red = 255, 0, 0
    salmon = 250, 128, 114
    tomato = 255, 99, 71
    orange = 255, 165, 0
    yellow_green = 154, 205, 50
    lime = 0, 255, 0
    dark_turquoise = 0, 206, 209
    deep_sky_blue = 0, 191, 255
    blue = 0, 0, 255
    dark_orchid = 153, 50, 204
    crimson = 220, 20, 60
    burlywood = 222, 184, 135
    khaki = 240, 230, 140
    medium_sea_green = 60, 179, 113

class Scene:
    """ A container class for Character and View management. """
    def __init__(self, backgroundColor=(0,0,0)):
        self.backgroundColor = backgroundColor
        self.currentView = 'default'
        self.views = {}
        self.views['default'] = {'x':0,'y':0,'width':800,'height':600}
        self.characters = []
        self.lastUpdateTime = 0
    def addView(self, view_name, x, y, width, height):
        """ Add a new view to the scene by specifying its name, coordinates and size. """
        self.views[view_name] = {'x': x, 'y':y, 'width': width, 'height':height}
    def resizeView(self, view_name, width, height):
        self.views[view_name] = {'x': self.views[view_name]['x'], 'y': self.views[view_name]['y'], 'width': width, 'height':height}
    def moveView(self, view_name, newX, newY):
        self.views[view_name] = {'x': newX, 'y': newY, 'width': self.views[view_name]['width'], 'height':self.views[view_name]['height']}
    def autoScrollView(self, x, y, milliseconds):
        """ Move the current view by x and y every interval of specified milliseconds. """
        timed = time.time()*1000
        if ( (timed- self.lastUpdateTime)> milliseconds):
            self.moveView(self.currentView, self.views[self.currentView]['x']+x, self.views[self.currentView]['y']+y)
            self.lastUpdateTime = timed
    def addCharacters(self, new_characters):
        """ Add Character objects to the Scene. """
        if isinstance(new_characters, list):
            for character in new_characters:
                self.characters.append(character)
        else:
            self.characters.append(new_characters)
    def setView(self, view):
        """ Set the current view of the Scene. """
        self.currentView = view
    def getView(self):
        """ Return the current view of the Scene as a dict. """
        return self.views[self.currentView]
    def setBackgroundColor(self, color):
        """ Set the scene background color as (R, G, B). """
        self.backgroundColor = color
    def updateScene(self, screen):
        """ Draw the objects within the current Scene view to a Pygame Display. """
        screen.fill(self.backgroundColor)
        for character in self.characters:
            bottom = character.y + character.height
            right = character.x + character.width
            if (bottom < self.views[self.currentView]['y']):
                continue
            if (character.y > (self.views[self.currentView]['y']+self.views[self.currentView]['height'])):
                continue
            if (right < self.views[self.currentView]['x']):
                continue
            if (character.x > (self.views[self.currentView]['x']+self.views[self.currentView]['width'])):
                continue
            screen.blit(character.getImage(), character.getRect().move(-self.views[self.currentView]['x'],-self.views[self.currentView]['y']))

class Animation:
    """ A container class for Pygame Image management. """
    def __init__(self, images=None):
        self.index = 0
        self.frames = []
        if (images!=None):
            if isinstance(images, list):
                for image in images:
                    self.frames.append(pygame.image.load(image))
            else:
                if images[-1]=='/':
                    image_dir = os.listdir(images)
                    for image in image_dir:
                        self.frames.append(pygame.image.load(images+image))
                else:
                    self.frames.append(pygame.image.load(images))

    def addFrames(self, images):
        """ Add frames to the animation. """
        if isinstance(images, list):
            for image in images:
                self.frames.append(pygame.image.load(image))
        else:
            self.frames.append(pygame.image.load(images))

    def takeFrame(self):
        """ Return the next frame in the animation sequence. """
        index = self.index
        if (self.index<len(self.frames)-1):
            self.index += 1
        else:
            self.index = 0
        return self.frames[index]

    def firstFrame(self):
        """ Return the first frame of the animation sequence. """
        return self.frames[0]
    

class Character:
    """ A 2D sprite class for handling motion and collisions. """
    def __init__(self, animation):
        self.animation = animation
        self.current_frame = self.animation.firstFrame()
        self.rect = self.animation.firstFrame().get_rect()

        self.lastUpdateTime = 0
        self.lastUpdateAnimTime = 0
        self.colliders = []

        self.x = self.rect.left
        self.y = self.rect.top
        self.height = self.rect.height
        self.width = self.rect.width      

        self.xvel = 0
        self.yvel = 0

        self.xacc = 0
        self.yacc = 0

    def setSize(self, new_width, new_height):
        self.height = new_height
        self.width = new_width

    def setPosition(self, newX, newY):
        self.x = newX
        self.y = newY
        
    def addColliders(self, others):
        if isinstance(others, list):
            for other in others:
                self.colliders.append(other)
        else:
            self.colliders.append(others)

    def Collide(self, other):
        #Define anchors of self
        left = self.x
        right = self.x + self.width
        top = self.y
        bottom = self.y + self.height
        #Define anchors of other
        otherL = other.x
        otherR = other.x + other.width
        otherT = other.y
        otherB = other.y + other.height

        #Left/ Right Collision Testing
        if not (top > otherB or bottom < otherT ):
            if (self.xvel>0):
                if (right == otherL):
                    self.xvel = 0
                if (right < otherL):
                    if (right+self.xvel > otherL):
                        self.xvel = otherL - right
            if (self.xvel<0):
                if (left == otherR):
                    self.xvel = 0
                if (left > otherR):
                    if (left+self.xvel < otherR):
                        self.xvel = left - otherR

        #Top/ Bottom Collision Testing
        if not (left > otherR or right < otherL ):
            if (self.yvel>0):
                if (bottom == otherT):
                    self.yvel = 0
                if (bottom < otherT):
                    if (bottom+self.yvel > otherT):
                        self.yvel = otherT - bottom
            if (self.yvel<0):
                if (top == otherB):
                    self.yvel = 0
                if (top > otherB):
                    if (top+self.yvel < otherB):
                        self.yvel = otherB - top


    def checkCollisionByType(self, other, direction='bottom'):
        """ Returns True if colliding with an instance of specified Character """
        return (isinstance(self.checkCollision(other,direction),type(other)))

    def checkCollision(self, other, direction='bottom'):
        #Define anchors of self
        left = self.x
        right = self.x + self.width
        top = self.y
        bottom = self.y + self.height
        #Define anchors of other
        otherL = other.x
        otherR = other.x + other.width
        otherT = other.y
        otherB = other.y + other.height

        if direction=='left':
            if (left == otherR) and (not (top > otherB or bottom < otherT )):
                return other
        if direction=='right':
            if (right == otherL) and (not (top > otherB or bottom < otherT )):
                return other

        if direction=='top':
            if (top == otherB) and (not (left > otherR or right < otherL )):
                return other

        if direction=='bottom':
            if (bottom == otherB) and (not (left > otherR or right < otherL )):
                return other
        return None 


    def updateMotion(self):
        if (len(self.colliders)>0):
            for collider in self.colliders:
                self.Collide(collider) 
        self.x += self.xvel
        self.y += self.yvel
        self.xvel += self.xacc
        self.yvel += self.yacc

    def autoUpdateMotion(self, milliseconds):
        timed = time.time()*1000
        if ( (timed- self.lastUpdateTime)> milliseconds):
            self.updateMotion()
            self.lastUpdateTime = timed
        
    def autoUpdateFrame(self, milliseconds):
        timed = time.time()*1000
        if ( (timed- self.lastUpdateAnimTime)> milliseconds):
            self.current_frame = self.animation.takeFrame()
            self.lastUpdateAnimTime = timed
        
    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def getImage(self):
        return self.current_frame

