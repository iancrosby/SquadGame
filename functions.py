__author__ = 'iwcrosby'

import math
import terrain
import pygame

# Setting up some useful functions.
def check_collision(p, co):
    '''Check if position p collides with object co'''

    if (p[0] >= co.collision[0][0]) and (p[0] <= co.collision[1][0]) and (p[1] >= co.collision[0][1]) and (p[1] <= co.collision[1][1]):
        return True

    return False


class creature:
    '''A clickable creature. Coordinate tuple p is the location. w and h are the width and height.'''

    def __init__(self, w=1, h=1, p=(0,0)):

        self.update_coordinates(w, h, p)
        self.speed = 3
        self.range = 15
        self.attk_cooldown = 20
        self.attk_cooldown_t = 0
        self.attk_len = 4
        self.attk_len_t = 0
        self.hp = 10
        self.damage = 2

    def load_image(self, filepath):
        '''Assign a sprite to be used for this creature'''

        self.img = pygame.image.load(filepath).convert()
        self.img.set_colorkey(self.img.get_at((0,0))) #The colour of the top-left pixel is set as transparent


    def update_coordinates(self, w, h, p):

        #check that x, y, and p are the correct types
        if not (isinstance(w, int) and isinstance(h, int) and isinstance(p, tuple)):
            raise TypeError

        #set new coordinates and collision points
        self.coordinates = [w, h, (p[0], p[1])]
        self.draw_coordinates = [p[0]-(float(w)/2), p[1]-(float(w)/2), w, h]
        #collision points set as top left position and bottom right position
        self.collision = (p, (p[0]+w, p[1]+h))

    def label(self, text):
        '''Add a label to a box'''

        font = pygame.font.Font(None, 25)
        self.text = font.render(text,True,black)

    def move(self, destination, m):
        '''Attempt to move to destination on map m.'''

        speed = self.speed
        w, h, (p_x, p_y) = self.coordinates

        diff_x = destination[0]-p_x
        diff_y = destination[1]-p_y
        hyp = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2))

        if hyp > speed:
            move_x = diff_x * speed / hyp
            move_y = diff_y * speed / hyp
            new_coords = (p_x+move_x, p_y+move_y)
        else:
            new_coords = destination

        if find_terrain((new_coords),m).passable == False:
            pass
        else:
            self.update_coordinates(w, h, new_coords)

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
    diff_x = float(obj1.coordinates[2][0]) - obj2.coordinates[2][0]
    diff_y = float(obj1.coordinates[2][1]) - obj2.coordinates[2][1]
    hyp = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2))
    return hyp

def find_terrain(p, m):
    '''Returns the terrain object that occupies coordinates p, on map m'''

    if p[0]<581 and p[1]<581:
        index_x = int(p[0]/20)
        index_y = int(p[1]/20)
        return m.grid[index_y][index_x]
    else:
        return m.grid[0][0]



class Map(object):

    def __init__(self):

        map_grid = []
        count1 = 0
        count2 = 0
        while count1 < 30:
            map_grid.append([])
            while count2 < 30:
                map_grid[count1].append(terrain.Terrain())
                count2 += 1
            count1 += 1
            count2 = 0

        self.grid = map_grid



if __name__ == "__main__":
    #some light testing
    test_box = creature(100, 100, (50,50))
    test_position_true = (60, 60)
    test_position_false = (151, 151)
    tests_passed = True
    test_w, test_h, test_p = 10, 10, (200,200)
    test_creature = creature(test_w, test_h, test_p)
    test_destination = (250,250)


    if not check_collision(test_position_true, test_box):
        raise AssertionError
        tests_passed = False

    if check_collision(test_position_false, test_box):
        raise AssertionError
        tests_passed = False

    test_creature.move(test_destination)
    '''if not (test_creature.coordinates[2][0] == test_p[0] and test_creature.coordinates[2][1] == test_p[1]+1):
        print test_creature.coordinates[2]
        raise AssertionError
        tests_passed = False'''

    print "Tests Passed = " + str(tests_passed)

#NEXT: write tests for move method