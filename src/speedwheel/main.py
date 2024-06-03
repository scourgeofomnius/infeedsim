import pygame
import pymunk
import pymunk.pygame_util
import math
import sys
import time

from variables import *
from classes import *

pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = 1920,800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kinematics approximation ")

PEs = []

def run(window, width, height):
    run           = True
    clock         = pygame.time.Clock()
    fps           = 240
    dt            = 1/fps
    boards         = []

    space         = pymunk.Space()
    space.gravity = (0,9.81 * fps)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    dealer1PE = Sensor((WIDTH/2-10, HEIGHT/2- 100),
                 (WIDTH/2-10, HEIGHT/2 + 30), 
                 1, 
                 space, 
                 8,
                 (speedup_position -10, tc_height + 190),
                 startdebounce=.1)
    boardGen = Sensor((WIDTH/2-140, HEIGHT/2 -100),
                     (WIDTH/2-140, HEIGHT/2+100),
                     13,
                     space,
                     14,
                     (),
                     startdebounce=.1)

    PEs = [dealer1PE, boardGen]
    boards =[]

    speed = SpeedupWheel((WIDTH/2, HEIGHT/2), 40, space)
    speed.stop.downtime = .45
    chain = Chain((WIDTH/2-300, HEIGHT/2), (WIDTH, HEIGHT/2),35, space, 3)
    board = Board((WIDTH/2-200, (HEIGHT/2)-100), 0, space)
    starttime = time.time()

    while run:
        el = time.time()
        if el - starttime > 1:
            print(board.body.kinetic_energy)
            starttime = el

        if dealer1PE.blocked:
            speed.stop.deal(el)
        if speed.stop.state == "down":
            speed.stop.deal(el)
        else:
            pass

        if not boardGen.blocked:
            if el - boardGen.starttime > .3:
                boards.append(Board((WIDTH/2 -140, HEIGHT/2-100), (0,0), space))
                boardGen.starttime = el


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
        
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
            #    speed1.stop.body.position = (speedup_position, tc_height)
                pass

        window.fill(white)
        space.debug_draw(draw_options) 
        for p in PEs:
            p.update(el)
            p.draw_register(window)

        pygame.display.update()

        space.step(dt)
        clock.tick(fps)

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
