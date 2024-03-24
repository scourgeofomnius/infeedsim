import pygame
import pymunk
import pymunk.pygame_util
import math
import sys

from classes import *
from cols import *


pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
mu = 2
objects = []


tc_height = 200
tc_width = 70 * scale
decline_angle = 180 - 23.4
decline_length = 69*scale
decline_start_y = tc_height
decline_end_y = (-1*(int(decline_length*math.sin(decline_angle)))) + tc_height
decline_start_x = tc_width
decline_end_x = decline_length + tc_width
deck2dealer_start_x = decline_end_x
deck2dealer_start_y = decline_end_y
deck2dealer_end_x = deck2dealer_start_x + int((85 * scale))
deck2dealer_end_y = deck2dealer_start_y
deck2_end_x = deck2dealer_end_x + int((45*scale))
deck2_start_y = deck2dealer_end_y
deck2_start_x = deck2dealer_end_x
deck2_end_y = deck2_start_y
speedup_position = tc_width - (18 * scale)
dealer2_position = deck2_end_x - (45 * scale)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kinematics approximation ")

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space, window,draw_options):
    window.fill("white")
    space.debug_draw(draw_options) 
    pygame.display.update()
    



def create_wall(space, x,y,width):
    shape = pymunk.Segment(space.static_body, x, y, width)
    shape.body.position = 0,0
    shape.friction = mu
    space.add(shape)



def run(window, width, height):
    run           = True
    clock         = pygame.time.Clock()
    fps           = 240
    dt            = 1/fps
    boards         = []

    space         = pymunk.Space()
    space.gravity = (0,981)

    create_wall(space, (deck2_end_x, deck2_end_y-10),(deck2_end_x, deck2_end_y-50), 10) 

    #create_belt(space)
    tc       = Chain((-50, tc_height),(tc_width, tc_height), 10, space, 2)
    decline  = Chain((decline_start_x,decline_start_y),(decline_end_x,decline_end_y), 10, space,6)
    d2dealer = Chain((deck2dealer_start_x, deck2dealer_start_y),(deck2dealer_end_x, deck2dealer_end_y), 10, space,5)
    d2       = Chain((deck2_start_x,deck2_start_y),(deck2_end_x,deck2_end_y), 10, space, 5)

    speed1   = SpeedupWheel((speedup_position, tc_height),15, space)
    speed2   = SpeedupWheel((dealer2_position, deck2_start_y),15, space)
    #stop1    = Stop((speedup_position, tc_height-10), (2,30),space)

    top_chain_handler            = space.add_collision_handler(1,2)
    top_chain_handler.begin      = top_chain_begin
    top_chain_handler.pre_solve  = top_chain_pre
    top_chain_handler.post_solve = top_chain_post
    top_chain_handler.separate   = top_chain_separate
    
    deck2_handler            = space.add_collision_handler(1,5)
    deck2_handler.begin      = deck2_begin
    deck2_handler.pre_solve  = deck2_pre
    deck2_handler.post_solve = deck2_post
    deck2_handler.separate   = deck2_separate

    speedup_handler            = space.add_collision_handler(1,3)
    speedup_handler.begin      = speedup_begin
    speedup_handler.pre_solve  = speedup_pre
    speedup_handler.post_solve = speedup_post
    speedup_handler.separate   = speedup_separate

    decline_handler            = space.add_collision_handler(1,6)
    decline_handler.begin      = decline_begin
    decline_handler.pre_solve  = decline_pre
    decline_handler.post_solve = decline_post
    decline_handler.separate   = decline_separate
    

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None

    for x in range(0,6): 
        boards.append(Board((x*board_width, tc_height-board_height), (0,0), space))
        #create_object(space, 10, (x * 70, tc_height-board_height))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()
                speed1.stop.body.position = (speedup_position, tc_height+20)
            if event.type == pygame.MOUSEBUTTONUP:
                speed1.stop.body.position = (speedup_position, tc_height)

        draw(space,window, draw_options)
        space.step(dt)
        clock.tick(fps)
        

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
