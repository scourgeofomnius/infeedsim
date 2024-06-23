import pymunk
from limits import *
#top chain stuff
def top_chain_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc
    return True
def top_chain_pre(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def top_chain_post(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc
    #print(velocity_at_local_point)
    return True
def top_chain_separate(arbiter, space, data):
    return True

def top2_chain_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc2
    return True
def top2_chain_pre(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc2
    arbiter.shapes[0].body.apply_impulse_at_local_point((8, 0),(0,0))
    return True
def top2_chain_post(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc2
    #print(velocity_at_local_point)
    return True
def top2_chain_separate(arbiter, space, data):
    return True

#decline stuff
def decline_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_decline
    return True
def decline_pre(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_decline
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def decline_post(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_decline
    #print(velocity_at_local_point)
    return True
def decline_separate(arbiter, space, data):
    return True

def declinestop_begin(arbiter, space, data):
    #arbiter.shapes[0].body.velocity_func = limit_velocity_declinestop
    return True
def declinestop_pre(arbiter, space, data):
    #arbiter.shapes[0].body.velocity_func = limit_velocity_declinestop
    if arbiter.shapes[0].body.velocity[0] > 0:
        arbiter.shapes[0].body.apply_impulse_at_local_point((-2.7, 0),(0,0))
    return True
def declinestop_post(arbiter, space, data):
    #arbiter.shapes[0].body.velocity_func = limit_velocity_zero
    #print(velocity_at_local_point)
    return True
def declinestop_separate(arbiter, space, data):
    return True

#deck two stuff
def deck2_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
    return True
def deck2_pre(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def deck2_post(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    #print(velocity_at_local_point)
    return True
def deck2_separate(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True

#speedup wheel stuff
def speedup_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_speedup
    return True
def speedup_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((16.67, 0),(0,0))
    return True
def speedup_post(arbiter, space, data):
    #print(velocity_at_local_point)
    pass
def speedup_separate(arbiter, space, data):
    pass


#deck two stuff
def intermediate_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_zero
    return True
def intermediate_pre(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_zero 
    return True
def intermediate_post(arbiter, space, data):
    #print(velocity_at_local_point)
    return True
def intermediate_separate(arbiter, space, data):
    return True
