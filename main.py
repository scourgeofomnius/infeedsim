import pygame
import pymunk
import time  
import pygame
from pygame import gfxdraw
from pygame.locals import *
import pygame.mixer
import time
import re
import pymunk.pygame_util
from pymunk import Vec2d
import sys

pygame.init()

font = pygame.font.SysFont(None, 30)

white = (255, 255, 255)
green = (0, 255, 0)
blue = (32, 187, 210)
black = (0,0,0)
grey = (110,110,110)
red = (255,0,0)
yellow = (252,228,13)

FPS = 50
clock = pygame.time.Clock()

screenwidth = 1000
screenheight = 1000

screen = pygame.display.set_mode((screenwidth, screenheight))
space = pymunk.Space()

class Board:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.body.friction = 1
        self.poly = pymunk.Poly.create_box(self.body, (self.w, self.h))
        self.poly.mass = 1
        space.add(self.body, self.poly)

class Chain:
    def __init__(self, x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.body.velocity = (20, 0)
        self.body.friction = 1
        self.poly = pymunk.Poly.create_box(self.body, (self.w, self.h))
        self.poly.mass = 100
        space.add(self.body, self.poly)
        

class Line:
    def __init__(self, x, y, radius) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, self.x), (self.y, self.x), self.radius)
        space.add(self.body,self.shape)



if __name__ == "__main__":
    pymunk.pygame_util.positive_y_is_up = True
    space.gravity = 0,-981 
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    board = Board(500,500, 30, 30)
    line = Line(100, 700, 10)
    chain = Chain(500, 150, 500, 10)
    
    print_options = pymunk.SpaceDebugDrawOptions()   

    while True:
        screen.fill(white)
        space.step(1/FPS)
        #pygame.draw.rect(screen, (255, 0 ,0), (int(body.position[0]), int(body.position[1])), (30, 30))
        space.debug_draw(draw_options)
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)
