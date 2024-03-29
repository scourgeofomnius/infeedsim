import pymunk
from limits import *
#top chain stuff
def top_chain_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_tc
    return True
def top_chain_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def top_chain_post(arbiter, space, data):
    #print(velocity_at_local_point)
    pass
def top_chain_separate(arbiter, space, data):
    pass

#decline stuff
def decline_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_decline
    return True
def decline_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def decline_post(arbiter, space, data):
    #print(velocity_at_local_point)
    pass
def decline_separate(arbiter, space, data):
    pass

#deck two stuff
def deck2_begin(arbiter, space, data):
    arbiter.shapes[0].body.velocity_func = limit_velocity_deck2
    return True
def deck2_pre(arbiter, space, data):
    arbiter.shapes[0].body.apply_impulse_at_local_point((2.93, 0),(0,0))
    return True
def deck2_post(arbiter, space, data):
    #print(velocity_at_local_point)
    pass
def deck2_separate(arbiter, space, data):
    pass

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


