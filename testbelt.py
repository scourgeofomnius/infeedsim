import pygame
import pymunk
import pymunk.pygame_util
import math
import sys

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
print(decline_end_y)


board_width = 5.5 * scale
board_height = 2.5 * scale

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
    

def limit_velocity(body, gravity, damping, dt):
    max_velocity = 500
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale

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
    def __init__(self, pos1, pos2, width, space):
        self.width = width
        self.shape = pymunk.Segment(space.static_body, pos1, pos2, width)
        self.shape.body.position = 0,0
        self.shape.friction = mu
        self.shape.collision_type = 2
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
        self.body.velocity_func = limit_velocity
        self.shape = pymunk.Poly.create_box(self.body, size = (board_width,board_height))
        self.shape.mass = 1
        self.shape.color = (222,174,91,100)
        self.shape.body.friction = mu
        self.shape.collision_type = 1
        space.add(self.body,self.shape)

def create_belt(space):
    belts = [
        [(0,tc_height), (tc_width,tc_height), 10],
        [(decline_start_x,decline_start_y), (decline_end_x,decline_end_y), 10],
        [(deck2dealer_start_x,deck2dealer_start_y), (deck2dealer_end_x,deck2dealer_end_y), 10],
        [(deck2_start_x,deck2_start_y), (deck2_end_x,deck2_end_y), 10],
    ]

    for pos_1, pos_2, width in belts:
        shape = pymunk.Segment(space.static_body,pos_1, pos_2, width) 
        shape.body.position = 0,0
        shape.friction = mu
        space.add(shape)

def create_wall(space, x,y,width):
    shape = pymunk.Segment(space.static_body, x, y, width)
    shape.body.position = 0,0
    shape.friction = mu
    space.add(shape)

def create_object(space, mass, pos):
    body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
    body.position = pos
    body.velocity_func = limit_velocity
    shape = pymunk.Poly.create_box(body, size = (board_width,board_height))
    shape.mass = mass
    shape.color = (255,0,0, 100)
    shape.body.friction = mu
    shape.collision_type = 1
    #shape.body.velocity = (80,0)
    space.add(body,shape)
    return shape

def chain_begin(arbiter, space, data):
    print(arbiter)
    #angle = calculate_angle(*)
    #force = calculate_distance(*line) * 50
    #fx = math.cos(angle) * force
    #fy = math.sin(angle) * force
    return True
def chain_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((.5, 0),(0,0))
    return True
def chain_post(arbiter, space, data):
    #print(velocity_at_local_point)
    pass
def chain_separate(arbiter, space, data):
    pass

def speedup_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((5, 0),(0,0))




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
    tc       = Chain((-50, tc_height),(tc_width, tc_height), 10, space)
    decline  = Chain((decline_start_x,decline_start_y),(decline_end_x,decline_end_y), 10, space)
    d2dealer = Chain((deck2dealer_start_x, deck2dealer_start_y),(deck2dealer_end_x, deck2dealer_end_y), 10, space)
    d2       = Chain((deck2_start_x,deck2_start_y),(deck2_end_x,deck2_end_y), 10, space)

    speed1   = SpeedupWheel((speedup_position, tc_height),15, space)
    speed2   = SpeedupWheel((dealer2_position, deck2_start_y),15, space)
    #stop1    = Stop((speedup_position, tc_height-10), (2,30),space)

    chain_handler            = space.add_collision_handler(1,2)
    chain_handler.begin      = chain_begin
    chain_handler.pre_solve  = chain_pre
    chain_handler.post_solve = chain_post
    chain_handler.separate   = chain_separate

    speedup_handler            = space.add_collision_handler(1,3)
    speedup_handler.begin      = chain_begin
    speedup_handler.pre_solve  = speedup_pre
    speedup_handler.post_solve = chain_post
    speedup_handler.separate   = chain_separate
    

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
