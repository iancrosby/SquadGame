__author__ = 'iwcrosby'

import pygame
from pygame.locals import *
from functions import *
pygame.init()


#Setting up some initialization stuff
done=False
size = [1024,768]
screen=pygame.display.set_mode(size)
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

my_dude = creature(10,10,(50,50))
my_dude.speed = 5
my_dude.range = 60
my_dude.load_image("images/metal_gear_frame_1.png")
zombie1 = creature(10,10,(400,400))
zombie2 = creature(10,10,(550,300))
zombie3 = creature(10,10,(350,500))
zombie2.speed = 2
zombie3.speed = 2.5
zombie_filepath = "images/zombie_frame_1.png"
zombie1.load_image(zombie_filepath)
zombie2.load_image(zombie_filepath)
zombie3.load_image(zombie_filepath)

player_list.append(my_dude)
zombie_list.append(zombie1)
zombie_list.append(zombie2)
zombie_list.append(zombie3)

destination = (50,50)

lose = False

# Set up the map
map1 = Map()
map1.grid[10][10] = terrain.Wall1()
map1.grid[10][11] = terrain.Wall1()
map1.grid[10][12] = terrain.Wall1()

# -------- Main Program Loop -----------
while done==False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

    #Reset to basic state


    for event in pygame.event.get(): # User did something
        if event.type == QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                destination = event.pos

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
        if player.coordinates[2] != destination:
            player.move(destination, map1)

    # zombies chase
    for obj in zombie_list:
        obj.move(my_dude.coordinates[2], map1)

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
            pygame.draw.rect(screen, obj.colour, [trn_x, trn_y, 20, 20], 0)
            trn_x += 20
        trn_y += 20
        trn_x = 0

    #draw player creatures
    for obj in player_list:
        screen.blit(obj.img, (obj.draw_coordinates[0], obj.draw_coordinates[1]))
        #draw attacks of player creatures
        if obj.attk_len_t > 0 and obj.attacking != None:
            pygame.draw.line(screen, blue, obj.coordinates[2], obj.attacking.coordinates[2], 3)

    # draw zombies
    for zombie in zombie_list:
        screen.blit(zombie.img, (zombie.draw_coordinates[0], zombie.draw_coordinates[1]))
        # draw zombie attacks
        if zombie.attk_len_t > 0 and zombie.attacking != None:
            pygame.draw.line(screen, red, zombie.coordinates[2], zombie.attacking.coordinates[2], 3)

    # draw dead creatures
    for obj in dead_list:
        pygame.draw.ellipse(screen, red, obj.draw_coordinates, 0)

    #draw a bunch of text. Mostly for debugging now.
    font = pygame.font.Font(None, 25)
    hp_text = font.render("HP = "+str(my_dude.hp),True,black)

    screen.blit(hp_text, (20, 20))


    #Game lose text
    if lose == True:
        text = font.render("You were eaten.",True,black)
        screen.blit(text, (400, 400))


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    pygame.display.flip()


    # Limit to 30 frames per second
    clock.tick(30)