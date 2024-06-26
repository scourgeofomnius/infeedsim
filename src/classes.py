import pymunk
from collections import OrderedDict
import pygame
import time
from variables import *
pygame.init()
default_font = pygame.font.get_default_font()
font = pygame.font.Font(default_font, 20)

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
    def __init__(self, pos, dims,space, downtime=.18, uptime=.5):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size=(dims))
        self.shape.color=(0,0,0,100)
        self.shape.body.friction = mu
        self.shape.collision_type=4
        space.add(self.body, self.shape)
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
        self.body  = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
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
        self.shape.body.friction = 1
        self.shape.collision_type = 1
        space.add(self.body,self.shape)
        self.start = time.time()

    def removeBoard(self, space):
        space.remove(self.body)
        space.remove(self.shape)
class Lug:
    def __init__(self, pos, dims, space):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size = (10,20))
        self.shape.mass = 1
        self.shape.color = (57,57,57,100)
        self.shape.body.friction = .3
        self.shape.collision_type = 100
        space.add(self.body,self.shape)
        self.start = time.time()

    def removeLug(self, space):
        space.remove(self.body)
        space.remove(self.shape)
    
    def moveLug(self):
        self.body.velocity = (100,0)
        if self.body.position[0] > decline_start_x:
            self.body.angle = 15 * math.pi/180
            self.body.velocity = (100,15.6)
        if self.body.position[0] > decline_end_x:
            self.body.position = (self.body.position[0], self.body.position[1] + .1)
            self.body.angle = self.body.angle + 20
            self.body.velocity = (100,15.6)
        #self.body.position = ()
    def stopLug(self):
        self.body.velocity = (0,0)

class LugSensor:
    def __init__(self, pos1, pos2, width, space, ctype, regpos, stopdebounce = 0.08, startdebounce = 0.08):
        self.width = width
        self.shape = pymunk.Segment(space.static_body, pos1, pos2, width)
        self.shape.sensor = True
        self.shape.color = (0,0,255,100)
        self.shape.body.position = 0,0
        self.shape.friction = mu
        self.shape.collision_type = ctype
        space.add(self.shape)
        self.handler = space.add_collision_handler(100,self.shape.collision_type)
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


class TextRegister:
    def __init__(self, pos, color, data):
        self.pos = pos
        self.color = color
        self.font = font
        self.data = data
        self.data_register = [x for x in self.data]

    def drawRegister(self, window):
        for k,v  in enumerate(self.data_register):
            window.blit(font.render(v[0], True, v[1]), (self.pos[0], self.pos[1] + (k * 20)))

    def appendRegister(self, text,color=black):
        self.data_register.append(text)

    def clearRegister(self):
        self.data_register = [x for x in self.data]

    def changeRegister(self, value):
        self.data_register = [value]






