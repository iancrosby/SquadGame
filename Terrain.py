__author__ = 'iwcrosby'

import pygame
grey    = ( 180, 180, 180)
black    = (   0,   0,   0)

class Impass_Trn(object):

    def __init__(self):
        pass


class Terrain(object):

    def __init__(self, p):
        self.colour = grey
        self.p = p
        self.init2()

    def init2(self):
        pass

class Road1(Terrain):

    def init2(self):
        self.colour = grey

class Wall1(Terrain):

    def init2(self):
        self.colour = black


class Left_Wall(Terrain):

    def init2(self):
        self.colour = grey
        self.impass_trn = Impass_Trn()
        self.impass_trn.rect = pygame.Rect(self.p,(5,20))
        self.impass_trn.colour = black

class Corner_Wall(Terrain):

    def init2(self):
        self.colour = grey
        self.impass_trn = Impass_Trn()
        self.impass_trn.rect = pygame.Rect(self.p,(20,20))
        self.impass_trn.colour = black

class Top_Wall(Terrain):

    def init2(self):
        self.colour = grey
        self.impass_trn = Impass_Trn()
        self.impass_trn.rect = pygame.Rect(self.p,(20,5))
        self.impass_trn.colour = black

class Right_Wall(Terrain):

    def init2(self):
        self.colour = grey
        self.impass_trn = Impass_Trn()
        self.impass_trn.rect = pygame.Rect((self.p[0]+15,self.p[1]),(5,20))
        self.impass_trn.colour = black

class Bottom_Wall(Terrain):

    def init2(self):
        self.colour = grey
        self.impass_trn = Impass_Trn()
        self.impass_trn.rect = pygame.Rect((self.p[0],self.p[1]+15),(20,5))
        self.impass_trn.colour = black