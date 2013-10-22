__author__ = 'iwcrosby'

grey    = ( 180, 180, 180)
black    = (   0,   0,   0)

class Terrain(object):

    def __init__(self):
        self.colour = grey
        self.passable = True
        self.init2()

    def init2(self):
        pass

class Road1(Terrain):

    def init2(self):
        self.colour = grey
        self.passable = True

class Wall1(Terrain):

    def init2(self):
        self.colour = black
        self.passable = False

