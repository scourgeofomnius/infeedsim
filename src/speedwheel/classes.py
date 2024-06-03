import pymunk
import pygame
import pymunk.pygame_util
import time
from variables import *
from limits import *

pygame.init()
default_font = pygame.font.get_default_font()
font = pygame.font.Font(default_font, 20)
fps = 240
mu = 2

class Chain:
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

    def _begin(self, arbiter, space, data):
        arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
        return True
    def _pre(self, arbiter, space, data):
        arbiter.shapes[0].body.apply_impulse_at_local_point((2*fps, 0),(0,0))
        return True
    def _post(self, arbiter, space, data):
        #print(velocity_at_local_point)
        pass
    def _separate(self, arbiter, space, data):
        pass

class Board:
    def __init__(self, pos, dims, space):
        self.body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size = (board_width,board_height))
        self.shape.mass = 1
        self.shape.density = 1
        self.shape.color = (222,174,91,100)
        self.shape.body.friction = 1
        self.shape.collision_type = 1
        space.add(self.body,self.shape)
        self.start = time.time()

    def removeBoard(self, space):
        space.remove(self.body)
        space.remove(self.shape)


class Stop:
    def __init__(self, pos, dims,space, downtime=.18, uptime=.5):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size=(dims))
        self.shape.color=(0,0,0,100)
        self.shape.body.friction = 1
        self.shape.collision_type=4
        space.add(self.body, self.shape)
        self.handler = space.add_collision_handler(1,self.shape.collision_type)
        self.handler.begin = self._begin
        self.handler.pre_solve = self._pre
        self.handler.post_solve = self._post
        self.handler.separate = self._separate
        self.starttime = time.time()
        self.dealtime = time.time()
        self.startpos = pos
        self.downtime = downtime
        self.uptime = uptime
        self.state = "up"

    def deal(self, el):
        if self.state == "up":
            if el-self.starttime > self.uptime:
                self.body.position = (self.startpos[0], self.startpos[1]+20)
                self.state = "down"
                self.starttime = el

        if self.state == "down":
            if el - self.starttime > self.downtime:
                self.body.position = (self.startpos[0], self.startpos[1])
                self.state = "up"
                self.starttime = el

            
    def stop(self, el):
        self.body.position = (self.startpos[0], self.startpos[1])

    def _begin(self, arbiter, space, data):
        return True
    def _pre(self, arbiter, space, data):
        return True
    def _post(self, arbiter, space, data):
        #print(velocity_at_local_point)
        pass
    def _separate(self, arbiter, space, data):
        pass


class SpeedupWheel:
    def __init__(self, pos, radius, space):
        self.rotation_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body  = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = pos
        self.body.angular_velocity = 20
        self.shape = pymunk.Circle(self.body, radius, (0,0))
        self.shape.color = (255,94,0,100)
        self.shape.friction = 500
        self.shape.collision_type = 3
        space.add(self.body, self.shape)
        self.handler = space.add_collision_handler(1,self.shape.collision_type)
        self.handler.begin = self._begin
        self.handler.pre_solve = self._pre
        self.handler.post_solve = self._post
        self.handler.separate = self._separate
        self.stop = Stop(pos, (2,(radius*2+20)), space)


    def _begin(self, arbiter, space, data):
        return True
    def _pre(self, arbiter, space, data):
        arbiter.shapes[0].body.velocity_func = limit_velocity_speedup
        arbiter.shapes[0].body.apply_impulse_at_local_point((41*fps, 0),(0,0))
        return True
    def _post(self, arbiter, space, data):
        #print(velocity_at_local_point)
        pass
    def _separate(self, arbiter, space, data):
        pass

class Sensor:
    def __init__(self, pos1, pos2, width, space, ctype, regpos, stopdebounce = 0.08, startdebounce = 0.08):
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
        self.startdebounce = startdebounce
        self.stopdebounce = stopdebounce
        self.previous = False

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
        self.previous = self.blocked
        if el - self.stoptime > self.startdebounce:
            self.blocked = False
        elif el - self.starttime > self.stopdebounce:
            self.blocked = True


    def osr(self, value):
        if self.blocked == True and self.previous == False:
            return True
        return False

    def osf(self, value):
        if self.blocked == False and self.previous == True:
            return True
        return False


