__author__ = 'iwcrosby'

import pygame
from pygame.locals import *
from functions import *
pygame.init()


#Setting up some initialization stuff
done=False
scr_size = [1024,768]
screen=pygame.display.set_mode(scr_size)
pygame.display.set_caption("SquadGame")
clock=pygame.time.Clock()

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
d_grey   = (  60,  60,  60)

player_list = []
zombie_list = []
dead_list = []

selected = None

my_dude = creature(10,10,(50,50))
my_dude.speed = 2.5
my_dude.range = 60
my_dude.load_image("images/metal_gear_frame_1.png")

my_dude2 = creature(10,10,(100,50))
my_dude2.speed = 2.5
my_dude2.range = 60
my_dude2.load_image("images/metal_gear_frame_1.png")

zombie1 = creature(10,10,(400,400))
zombie2 = creature(10,10,(550,300))
zombie3 = creature(10,10,(350,500))
zombie2.speed = 1
zombie3.speed = 1.25
zombie_filepath = "images/zombie_frame_1.png"
zombie1.load_image(zombie_filepath)
zombie2.load_image(zombie_filepath)
zombie3.load_image(zombie_filepath)

player_list.append(my_dude)
player_list.append(my_dude2)
zombie_list.append(zombie1)
zombie_list.append(zombie2)
zombie_list.append(zombie3)

destination = (50,50)

lose = False

# Set up the map
map1 = Map(40, 30, 20)
#map1.grid[10][10] = terrain.Wall1()
#map1.grid[11][10] = terrain.Wall1()
#map1.grid[12][10] = terrain.Wall1()

map1.grid[12][11] = terrain.Corner_Wall((12*20,11*20))
map1.grid[12][12] = terrain.Left_Wall((12*20,12*20))
map1.grid[12][13] = terrain.Left_Wall((12*20,13*20))
map1.grid[12][14] = terrain.Left_Wall((12*20,14*20))
map1.grid[12][15] = terrain.Left_Wall((12*20,15*20))
map1.grid[12][16] = terrain.Left_Wall((12*20,16*20))
map1.grid[12][17] = terrain.Left_Wall((12*20,17*20))
map1.grid[12][18] = terrain.Corner_Wall((12*20,18*20))

map1.grid[13][11] = terrain.Top_Wall((13*20,11*20))
map1.grid[14][11] = terrain.Top_Wall((14*20,11*20))
map1.grid[15][11] = terrain.Top_Wall((15*20,11*20))
map1.grid[16][11] = terrain.Top_Wall((16*20,11*20))
map1.grid[17][11] = terrain.Top_Wall((17*20,11*20))

map1.grid[13][18] = terrain.Bottom_Wall((13*20,18*20))
map1.grid[14][18] = terrain.Bottom_Wall((14*20,18*20))
map1.grid[15][18] = terrain.Bottom_Wall((15*20,18*20))
map1.grid[16][18] = terrain.Bottom_Wall((16*20,18*20))
map1.grid[17][18] = terrain.Bottom_Wall((17*20,18*20))

map1.grid[18][11] = terrain.Corner_Wall((18*20,11*20))
map1.grid[18][12] = terrain.Right_Wall((18*20,12*20))

map1.grid[18][15] = terrain.Right_Wall((18*20,15*20))
map1.grid[18][16] = terrain.Right_Wall((18*20,16*20))
map1.grid[18][17] = terrain.Right_Wall((18*20,17*20))
map1.grid[18][18] = terrain.Corner_Wall((18*20,18*20))



# process list of impassable terrain. Eventually move into the map class in functions.py
impass_trn_list = []

for list in map1.grid:
    for trn in list:
        if hasattr(trn, 'impass_trn'):
            impass_trn_list.append(trn.impass_trn)

map1.impass_trn = impass_trn_list


clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while done==False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

    #Reset to basic state


    for event in pygame.event.get(): # User did something
        if event.type == QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for player in player_list:
                    if player.rect.collidepoint(event.pos):
                        selected = player
            if event.button == 3 and selected != None:
                selected.destination = event.pos

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # game over
    if my_dude.hp <= 0:
        lose = True

    # count down the timers for players
    for obj in player_list:
        if obj.attk_cooldown_t > 0:
            obj.attk_cooldown_t -= 1
        if obj.attk_len_t > 0:
            obj.attk_len_t -= 1

    # count down the timers for zombies
    for obj in zombie_list:
        if obj.attk_cooldown_t > 0:
            obj.attk_cooldown_t -= 1
        if obj.attk_len_t > 0:
            obj.attk_len_t -= 1

    # player move
    for player in player_list:
        player.move(player.destination, map1)

    # zombies chase
    for obj in zombie_list:
        obj.move(my_dude.rect.center, map1)

    # zombie attack
    for zombie in zombie_list:
        zombie.choose_target(player_list)
        if zombie.attacking != None and zombie.attk_cooldown_t < 1:
            zombie.attack(zombie.attacking)

    # my dude choose target
    for player in player_list:
        player.choose_target(zombie_list)
        if player.attacking != None and player.attk_cooldown_t < 1:
            player.attack(player.attacking)


    # kill off 0 hp creatures
    for zombie in zombie_list:
        if zombie.hp <= 0:
            dead_list.append(zombie)
            zombie_list.remove(zombie)

    for player in player_list:
        if player.hp <= 0:
            dead_list.append(player)
            player_list.remove(player)




    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    screen.fill(white)

    #draw terrain
    trn_x = 0
    trn_y = 0
    for mylist in map1.grid:
        for obj in mylist:
            pygame.draw.rect(screen, obj.colour, ((obj.p), (map1.tile_size, map1.tile_size)), 0)
            if hasattr(obj, 'impass_trn'):
                pygame.draw.rect(screen, obj.impass_trn.colour, obj.impass_trn.rect, 0)
            trn_y += map1.tile_size
        trn_x += map1.tile_size
        trn_y = 0

    # draw dead creatures
    for obj in dead_list:
        pygame.draw.ellipse(screen, red, obj.rect, 0)

    #draw selection circle
    if selected != None:
        pygame.draw
        s_w = selected.rect.w+4
        s_p = (selected.rect.centerx-(s_w/2)+1, selected.rect.bottom-13)
        pygame.draw.ellipse(screen, white, (s_p, (s_w, 13)), 2)

    #draw player creatures
    for obj in player_list:
        screen.blit(obj.img, (obj.coordinates))
        #draw attacks of player creatures
        if obj.attk_len_t > 0 and obj.attacking != None:
            pygame.draw.line(screen, blue, obj.rect.center, obj.attacking.rect.center, 3)

    # draw zombies
    for zombie in zombie_list:
        screen.blit(zombie.img, zombie.coordinates)
        # draw zombie attacks
        if zombie.attk_len_t > 0 and zombie.attacking != None:
            pygame.draw.line(screen, red, zombie.rect.center, zombie.attacking.rect.center, 3)



    #draw a bunch of text. Mostly for debugging now.
    font = pygame.font.Font(None, 25)
    hp_text = font.render("HP = "+str(my_dude.hp),True,black)
    fps_text = font.render("FPS = "+str(clock.get_fps()),True,black)
    screen.blit(hp_text, (20, 20))
    screen.blit(fps_text, (20, 40))


    #Game lose text
    if lose == True:
        text = font.render("You were eaten.",True,black)
        screen.blit(text, (400, 400))


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    pygame.display.flip()


    # Limit to 30 frames per second
    clock.tick(60)