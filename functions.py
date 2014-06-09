__author__ = 'iwcrosby'

import math
import terrain
import pygame

# Setting up some useful functions.


class creature:
    '''A clickable creature. Coordinate tuple p is the location. w and h are the width and height.'''

    def __init__(self, w=1, h=1, p=(0,0)):

        self.rect = pygame.Rect(p,(w,h))
        self.update_coordinates(p)
        self.speed = 1.5
        self.range = 15
        self.attk_cooldown = 20
        self.attk_cooldown_t = 0
        self.attk_len = 4
        self.attk_len_t = 0
        self.hp = 10
        self.damage = 2
        self.destination = p

    def load_image(self, filepath):
        '''Assign a sprite to be used for this creature'''

        self.img = pygame.image.load(filepath).convert()
        self.rect.size = self.img.get_bounding_rect().size
        self.img.set_colorkey(self.img.get_at((0,0))) #The colour of the top-left pixel is set as transparent

    def update_coordinates(self, p):

        #check that p is a tuple
        if not isinstance(p, tuple):
            raise TypeError

        #set new coordinates
        self.coordinates = p
        self.rect.topleft = p

    def label(self, text):
        '''Add a label to a box'''

        font = pygame.font.Font(None, 25)
        self.text = font.render(text,True,black)

    def move(self, destination, m):
        '''Attempt to move to destination on map m.'''

        destination = destination[0]-self.rect.w/2, destination[1]-self.rect.h/2
        speed = self.speed
        p = self.coordinates

        diff_x = destination[0]-p[0]
        diff_y = destination[1]-p[1]
        hyp = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2))

        if hyp > speed:
            move_x = diff_x * speed / hyp
            move_y = diff_y * speed / hyp
            new_coords = (p[0]+move_x, p[1]+move_y)

        else:
            new_coords = destination

        self.update_coordinates(new_coords)

        for trn in m.impass_trn:
            if trn.rect.colliderect(self.rect):
                self.update_coordinates(p) # Move back to old coordinates if new coordinates cause a collision.


    def choose_target(self, target_list):

        chosen_target = None
        min_target_dist = 100000
        for target in target_list:
            target_dist = distance(self,target)
            if target_dist < min_target_dist and target_dist < self.range:
                chosen_target = target
                min_target_dist = target_dist

        self.attacking = chosen_target
        return chosen_target


    def attack(self, target):

        self.attk_cooldown_t = self.attk_cooldown
        self.attk_len_t = self.attk_len
        self.attacking = target
        target.hp -= self.damage

def distance(obj1, obj2):
    diff_x = float(obj1.rect.centerx) - obj2.rect.centerx
    diff_y = float(obj1.rect.centery) - obj2.rect.centery
    hyp = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2))
    return hyp

def find_terrain(p, m):
    '''Returns the terrain object that occupies coordinates p, on map m, followed by any impassable terrain object.'''

    tsize = m.tile_size
    num_x = len(m.grid)
    num_y = len(m.grid[0])

    index_x = int(p[0]/tsize)
    index_y = int(p[1]/tsize)
    trn = m.grid[index_x][index_y]
    impass_trn = None

    if hasattr(trn, "impass_trn"):
        impass_trn = trn.impass_trn

    if index_x<num_x and index_y<num_y:
        return (trn, impass_trn)
    else:
        return (m.grid[0][0], None)



class Map(object):

    def __init__(self, num_tile_x=30, num_tile_y=30, tile_size=20):

        map_grid = []
        count1 = 0
        count2 = 0
        while count1 < num_tile_x:
            map_grid.append([])
            while count2 < num_tile_y:
                p = (tile_size*count1,tile_size*count2)
                map_grid[count1].append(terrain.Terrain(p))
                count2 += 1
            count1 += 1
            count2 = 0

        self.grid = map_grid
        self.tile_size = tile_size





if __name__ == "__main__":

    from pygame.locals import *
    pygame.init()
    scr_size = [1024,768]
    screen=pygame.display.set_mode(scr_size)

    #some light testing
    test_box = creature(100, 100, (50,50))
    test_position_true = (60, 60)
    test_position_false = (151, 151)
    tests_passed = True
    test_w, test_h, test_p = 10, 10, (200,200)
    test_creature = creature(test_w, test_h, test_p)
    test_destination = (250,250)
    #test_map = Map()



    #test_creature.move(test_destination, test_map)
    #test_creature.load_image("images/metal_gear_frame_1.png")
    #size = test_creature.rect.size
    '''if not (test_creature.coordinates[2][0] == test_p[0] and test_creature.coordinates[2][1] == test_p[1]+1):
        print test_creature.coordinates[2]
        raise AssertionError
        tests_passed = False'''

    print "Tests Passed = " + str(tests_passed)


#NEXT: write tests for move method