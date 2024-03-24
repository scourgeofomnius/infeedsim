import pymunk
import pygame
import time
pygame.init()
default_font = pygame.font.get_default_font()
font = pygame.font.Font(default_font, 20)
mu = 2
WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
board_width = 5.5 * scale
board_height = 2.5 * scale
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
grey = (110,110,110)
red = (255,0,0)
yellow = (252,228,13)
class Debounce:
    def __init__(self, dt, dtoff=.08):
        self.starttime = time.time()
        self.stoptime = time.time()
        self.state = False
        self.dt = dt
        self.dtoff = dtoff
        
    def check(self, el):
        if self.state:
            if el - self.starttime > self.dt:
                self.state = False
                self.stoptime = el
            return True 

    def set(self, el):
        if not self.state:
            if el - self.stoptime > self.dtoff:
                self.state = True
                self.starttime = el
                return False
        return True
        
class Stop:
    def __init__(self, pos, dims,space):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size=(dims))
        self.shape.color=(0,0,0,100)
        self.shape.body.friction = mu
        self.shape.collision_type=4
        space.add(self.body, self.shape)

class Chain:
    def __init__(self, pos1, pos2, width, space, ctype):
        self.width = width
        self.shape = pymunk.Segment(space.static_body, pos1, pos2, width)
        self.shape.body.position = 0,0
        self.shape.friction = mu
        self.shape.collision_type = ctype
        space.add(self.shape)

class Wall:
    def __init__(self, pos1, pos2, width, space, ctype):
        self.width = width
        self.shape = pymunk.Segment(space.static_body, pos1, pos2, width)
        self.shape.body.position = 0,0
        self.shape.friction = mu
        self.shape.collision_type = ctype
        space.add(self.shape)
        self.handler = space.add_collision_handler(1,self.shape.collision_type)
        self.handler.begin = self._begin
        self.handler.pre_solve = self._pre
        self.handler.post_solve = self._post
        self.handler.separate = self._separate
        self.starttime = time.time()
        self.allowpinch = False
        
#top chain stuff
    def _begin(self, arbiter, space, data):
        self.starttime = time.time()
        return True
    def _pre(self, arbiter, space, data):
        if self.starttime - time.time() > .3:
            self.allowpinch = True
        return True
    def _post(self, arbiter, space, data):
        #print(velocity_at_local_point)
        pass
    def _separate(self, arbiter, space, data):
        self.allowpinch = False
        pass

class SpeedupWheel:
    def __init__(self, pos, radius, space):
        self.body  = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius, (0,0))
        self.shape.color = (255,94,0,100)
        self.shape.friction = mu
        self.shape.collision_type = 3
        space.add(self.body, self.shape)
        self.stop = Stop(pos, (2,50), space)
        
class Board:
    def __init__(self, pos, dims, space):
        self.body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size = (board_width,board_height))
        self.shape.mass = 1
        self.shape.color = (222,174,91,100)
        self.shape.body.friction = mu
        self.shape.collision_type = 1
        space.add(self.body,self.shape)
        self.start = time.time()

    def removeBoard(self, space):
        space.remove(self.body)
        space.remove(self.shape)

class Sensor:
    def __init__(self, pos1, pos2, width, space, ctype, regpos):
        self.width = width
        self.shape = pymunk.Segment(space.static_body, pos1, pos2, width)
        self.shape.sensor = True
        self.shape.color = (0,0,255,100)
        self.shape.body.position = 0,0
        self.shape.friction = mu
        self.shape.collision_type = ctype
        space.add(self.shape)
        self.handler = space.add_collision_handler(1,self.shape.collision_type)
        self.handler.begin = self._begin
        self.handler.pre_solve = self._pre
        self.handler.post_solve = self._post
        self.handler.separate = self._separate
        self.blocked = False
        self.font = font
        self.data_register = ["blocked"]
        self.pos = pos1
        self.starttime = time.time()
        self.stoptime = time.time()

    def draw_register(self, window):
        color = red if self.blocked else green
        pygame.draw.circle(window, color, self.pos, 10, 5)
        #window.blit(font.render("".join(self.data_register), True, color),(self.pos[0],self.pos[1]-100))

    def clear_register(self):
        self.data_register = []

#top chain stuff
    def _begin(self, arbiter, space, data):
        self.starttime = time.time()
        return True
    def _pre(self, arbiter, space, data):
        self.stoptime = time.time()
        return True
    def _post(self, arbiter, space, data):
        #print(velocity_at_local_point)
        return True
    def _separate(self, arbiter, space, data):
        return True

    def update(self, el):
        if el - self.stoptime > .05:
            self.blocked = False
        else:
            self.blocked = True

