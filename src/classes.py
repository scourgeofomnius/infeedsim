import pymunk
import time
mu = 2
WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
board_width = 5.5 * scale
board_height = 2.5 * scale
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
        
class SpeedupWheel:
    def __init__(self, pos, radius, space):
        self.body  = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius, (0,0))
        self.shape.color = (255,0,0,100)
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


