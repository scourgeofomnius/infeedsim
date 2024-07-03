import pygame
from collections import OrderedDict
import pymunk
import pymunk.pygame_util
import math
import sys
import time

from variables import *
from classes import *
from cols import *



pygame.init()
space = pymunk.Space()

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

prepositions = []
with open('positions.txt', 'r')as f:
    for line in f:
        prepositions.append([float(x) for x in line.strip('\n').split(':')])
for v in prepositions:
    print(v)
def run(window, width, height):
    run           = True
    lugindex  = 0
    clock         = pygame.time.Clock()
    fps           = 60
    dt            = 1/fps
    boards         = []

    space         = pymunk.Space()
    space.gravity = (0,981)

    starttime = time.time()
    lugpositions = []
    #create_wall(space, (deck2_end_x, deck2_end_y-10),(deck2_end_x, deck2_end_y-50), 10) 
    pinch = Wall((deck2_end_x, deck2_end_y-10),
                 (deck2_end_x, deck2_end_y-50),
                 10,
                 space,
                 11)

    #create_belt(space)
    tc       = Chain((-50, tc_height),
                     (speedup_position, tc_height-3), 
                     10, 
                     space, 
                     2)
    t2       = Chain((speedup_position, tc_height),
                     (decline_start_x-2, tc_height), 
                     10, 
                     space, 
                     19)
    decline  = Chain((decline_start_x,decline_start_y),
                     (decline_end_x,decline_end_y), 
                     10, 
                     space,
                     6)
    d2dealer = Chain((deck2dealer_start_x, deck2dealer_start_y),
                     (deck2dealer_end_x, deck2dealer_end_y), 
                     10, 
                     space,
                     5)
    d2       = Chain((deck2_start_x,deck2_start_y),
                     (deck2_end_x,deck2_end_y), 
                     10, 
                     space, 
                     16)
    top_chain_handler            = space.add_collision_handler(1,2)
    top_chain_handler.begin      = top_chain_begin
    top_chain_handler.pre_solve  = top_chain_pre
    top_chain_handler.post_solve = top_chain_post
    top_chain_handler.separate   = top_chain_separate

    top2_chain_handler            = space.add_collision_handler(1,19)
    top2_chain_handler.begin      = top2_chain_begin
    top2_chain_handler.pre_solve  = top2_chain_pre
    top2_chain_handler.post_solve = top2_chain_post
    top2_chain_handler.separate   = top2_chain_separate
    
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

    deck_short_chain_handler = space.add_collision_handler(1,16)
    deck_short_chain_handler.begin      = deck2_begin
    deck_short_chain_handler.pre_solve  = deck2_pre
    deck_short_chain_handler.post_solve = deck2_post
    deck_short_chain_handler.separate   = deck2_separate

 
    declinestop_handler = space.add_collision_handler(1,20)
    declinestop_handler.begin      = declinestop_begin
    declinestop_handler.pre_solve  = declinestop_pre
    declinestop_handler.post_solve = declinestop_post
    declinestop_handler.separate   = declinestop_separate

    speed1   = SpeedupWheel((speedup_position, tc_height+2),15, space)
    speed1.stop.downtime = dealer_stop_downtime1
    speed1.stop.uptime = dealer_stop_uptime
#    dealer1_Pe_after = Sensor((speedup_position+(8*scale), tc_height - 100),
#                 (speedup_position+(8*scale), tc_height + 30), 
#                 1, 
#                 space, 
#                 7,
#                 (speedup_position +5, tc_height + 100))
    dealer1PE = Sensor((speedup_position-10, tc_height - 100),
                 (speedup_position-10, tc_height + 30), 
                 1, 
                 space, 
                 8,
                 (speedup_position -10, tc_height + 190),
                 startdebounce=.1)


    dealer2PE = Sensor((dealer2_position-10, deck2_start_y - 100),
                 (dealer2_position-10, deck2_start_y + 30), 
                 1, 
                 space, 
                 10,
                 (dealer2_position -5, deck2_start_y + 50),
                 startdebounce=.1)

    pinchPE = Sensor((deck2_end_x - 20, deck2_end_y - 100),
                     (deck2_end_x -20, deck2_end_y + 100),
                     1,
                     space,
                     12,
                     (deck2_end_x -10, deck2_end_y -100))

    boardGenPE = Sensor((50, tc_height-50),
                        (50, tc_height+50),
                        board_width,
                        space,
                        13,
                        (50, tc_height-100))

    deck2StopPe = Sensor((dealer2_position + (30*scale), deck2_start_y-100),
                         (dealer2_position + (30*scale), deck2_start_y+100),
                         4,
                         space,
                         15,
                         (dealer2_position + (30*scale), deck2_start_y-100),
                         stopdebounce=deck2full_delay)

    lugStartPe = LugSensor((decline_start_x + 100, decline_start_y -100),
                         (decline_start_x + 100, decline_start_y +100),
                         1,
                         space,
                         101,
                         (0,0),
                         stopdebounce=.01)


    lugEndPe = LugSensor((decline_end_x, decline_end_y -100),
                         (decline_end_x, decline_end_y +100),
                         1,
                         space,
                         102,
                         (0,0),
                         stopdebounce=0)
    dealerLugInterlockPe = LugSensor((decline_start_x+70, decline_start_y -100),
                         (decline_start_x+70, decline_start_y +100),
                         1,
                         space,
                         103,
                         (0,0),
                         stopdebounce=0)




    #PEs = [pinchPE,deck2StopPe,deck2fullPe,boardGenPE,pe3,dealer1_Pe_after,dealer1PE,dealer2PE]
    PEs = [dealerLugInterlockPe,pinchPE,deck2StopPe,boardGenPE,dealer1PE,lugStartPe,lugEndPe]

    #stop1    = Stop((speedup_position, tc_height-10), (2,30),space)

   

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None

    startcheck = True
    checkspeed1 = time.time()
    endcheck = True

    tc_values = [["Top Chain", black], 
                 [f"speed = {round(tc_max_speed/speed_scale)}ft/min", black]]

    dc_values = [["Decline Belt", black], 
                 [f"speed = {round(decline_max_speed/speed_scale)}ft/min",black]]
    deck2dealer_values = [["Deck2 Dealer Chains",black], 
                          [f"speed = {round(deck2_max_speed/speed_scale)}ft/min",black]]
    pinch_values = [["PichRoll",black],
                    [f"board process time: {board_process_time+.3}",red]]
    deck2_values = [["Deck 2 Short Chains",black], 
                    [f"speed = {round(deck2_max_speed/speed_scale)}ft/min",black]]

    tc_register = TextRegister((50, 600), black, tc_values)
    decline_register = TextRegister((350, 600), black, dc_values)
    deck2dealer_register = TextRegister((650, 600), black, deck2dealer_values)
    pinch_register = TextRegister((950, 600), black, pinch_values)
    deck2_register = TextRegister((1250, 600), black, deck2_values)
    dist1 = TextRegister((70*scale, 30), black, [[f"{round(70/12)}ft",red]])
    dist2 = TextRegister((decline_end_x, 30), black, [[f"{round((decline_end_x/scale)/12)}ft",red]])
    dist3 = TextRegister((deck2dealer_end_x, 30), black, [[f"{round((deck2dealer_end_x/scale)/12)}ft",red]])
    dist4 = TextRegister((deck2_end_x, 30), black, [[f"{round((deck2_end_x/scale)/12)}ft",red]])
    



    boardq = []
    boardreg = TextRegister((30, 30), black, [[str(len(boardq)),blue]])
    regs = [tc_register, 
            decline_register, 
            deck2dealer_register, 
            pinch_register,
            deck2_register,
            dist1,
            dist2,
            dist3,
            dist4,
            boardreg
            ]


    keepdeclinerunning = time.time()
    stopdecline = False
    stopdeal = False

    lugs = []
    lugPassedAllowDeal = True
    totallugdistance = prepositions[-1][0] - prepositions[0][0]
    print(totallugdistance)
    numoflugs = int(totallugdistance/(18*scale))
    for x in range(numoflugs-1):        
        offset = int(x * (18*scale))
        if offset > len(prepositions)-1:
            offset = len(prepositions)-1
        lugs.append(Lug((prepositions[offset][0], prepositions[offset][1]),(0,0),space))
        lugs[x].body.angle = prepositions[offset][2]
        #lugs[x].printLug()
    while run:
        el = time.time()
        #handle dealer 1
        for r in regs:
            r.clearRegister()
        
        #if el- lugStartPe.starttime > .1:
        #    lugPassedAllowDeal = True
        #    lugStartPe.starttime = el

        if dealerLugInterlockPe.osr(True):
            lugPassedAllowDeal = True
            lugStartPe.starttime = el


        if dealer1PE.blocked and not deck2StopPe.blocked and lugPassedAllowDeal:
            #if len(boardq) < boardqwidth:
            #stopdeal = True
            speed1.stop.deal(el)
            lugPassedAllowDeal = False
        #if dealer1_Pe_after.osf(True):
        #    boardq.append(1)
        if speed1.stop.state == "down":
            speed1.stop.deal(el)
            tc_register.appendRegister(["Dealing",green])
        else:
            tc_register.appendRegister(["Waiting",red])


        if deck2StopPe.osf(True):
            keepdeclinerunning = time.time()
            pass

        if el - keepdeclinerunning > 1:
            stopdecline = True

        if stopdecline:
            decline_handler.begin      = intermediate_begin
            decline_handler.pre_solve  = intermediate_pre
            decline_handler.post_solve = intermediate_post
            decline_handler.separate   = intermediate_separate
        else:
            for index, lug in enumerate(lugs):
                lug.stepLugPos(prepositions, index) 
                #lug.printLug()


        #    for lug in lugs:
        #        lug.stopLug()
        #else:
        #    for lug in lugs:
        #        lug.moveLug()
        #lugs[0].setLugPos(prepositions[lugindex-45])
        #if lugindex < len(prepositions) -1:
        #    lugindex += 1
        #else:
        #    lugindex = 0

        if not deck2StopPe.blocked:
            keepdeclinerunning = el
            stopdecline = False


        if deck2StopPe.osf(True):
            stopdecline = False
            deck2_handler.begin      = deck2_begin
            deck2_handler.pre_solve  = deck2_pre
            deck2_handler.post_solve = deck2_post
            deck2_handler.separate   = deck2_separate

            deck_short_chain_handler.begin = deck2_begin
            deck_short_chain_handler.pre_solve  = deck2_pre
            deck_short_chain_handler.post_solve = deck2_post
            deck_short_chain_handler.separate   = deck2_separate
        
            decline_handler.begin      = decline_begin
            decline_handler.pre_solve  = decline_pre
            decline_handler.post_solve = decline_post
            decline_handler.separate   = decline_separate

            top_chain_handler.begin      = top_chain_begin
            top_chain_handler.pre_solve  = top_chain_pre
            top_chain_handler.post_solve = top_chain_post
            top_chain_handler.separate   = top_chain_separate

            top2_chain_handler.begin      = top2_chain_begin
            top2_chain_handler.pre_solve  = top2_chain_pre
            top2_chain_handler.post_solve = top2_chain_post
            top2_chain_handler.separate   = top2_chain_separate
 

 

        #handle pinch
        if pinchPE.blocked:
            if el - pinchPE.starttime > .3+ board_process_time: 
                boards[0].removeBoard(space)
                boards.pop(0)
                pinchPE.starttime = el


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endtime = time.time()
                #with open('positions.txt', 'w') as f:
                #    for k,v in enumerate(lugpositions):
                #        f.write(f'{v[0]}:{v[1]}:{v[2]}\n')
                #    f.write(f'{(endtime - starttime)}')
                pygame.quit()
                sys.exit()    
        
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
            #    speed1.stop.body.position = (speedup_position, tc_height)
                pass

        #handl boardGen
        if not boardGenPE.blocked:
            if el - boardGenPE.starttime > .3:
                boards.append(Board((50, tc_height-board_height), (0,0), space))
                boardGenPE.starttime = el

#        if not lugStartPe.blocked:
#            if el -lugStartPe.starttime > 2:
#                lugs.append(Lug((decline_start_x, decline_start_y-20),(0,0),space))
#                lugStartPe.starttime = el

        #if lugStartPe.osr(True) or len(lugs) == 0:
        #    lugs.append(Lug((decline_start_x-20, decline_start_y-20),(0,0),space))


        #if lugEndPe.osf(True):
        #    if len(lugs)> 0:
        #        lugs[0].removeLug(space)
        #        lugs.pop(0)

        lugdistance = 0
        if len(lugs) > 2:
            x1 = round(lugs[0].body.position[0])
            x2 = round(lugs[1].body.position[0])
            y1 = round(lugs[0].body.position[1])
            y2 = round(lugs[1].body.position[1])
            lugdistance = round(math.sqrt((x1-x2)**2 + (y2-y1)**2)/scale,0)

        decline_register.appendRegister([str(lugdistance), blue])         
        if len(boards) > 0:
            if startcheck:
                if boards[0].body.position[0] > decline_start_x:
                    checkspeed1 = time.time()
                    startcheck = False
            if endcheck:
                if boards[0].body.position[0] > decline_end_x:
                    print(f"time to deck2dealer {(85 /(time.time() - checkspeed1))*5}")
                    endcheck = False
        if len(lugs) > 0:
            lugpositions.append([lugs[0].body.position[0], lugs[0].body.position[1], lugs[0].body.angle])

        window.fill(white)
        space.debug_draw(draw_options) 

        for PE in PEs:
            PE.update(el)
            PE.draw_register(window)

        #Osr must called right after update
        #if pe3.osf(True):
        #    if len(boardq) > 0:
        #        boardq.pop()
        
        #if deck2fullPe.blocked:
        #    boardq = [x for x in range(9)]

        boardreg.changeRegister([str(len(boardq)), blue])

        for r in regs:
            r.drawRegister(window)

        pygame.display.update()
        space.step(dt)
        clock.tick(fps)
        

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
