import pymunk
tc_max_speed = 70
deck2_max_speed = 30
decline_max_speed = 120
speedup_max_speed = 90

def limit_velocity_tc(body, gravity, damping, dt):
    max_velocity = tc_max_speed
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale
def limit_velocity_decline(body, gravity, damping, dt):
    max_velocity = decline_max_speed
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale
def limit_velocity_deck2(body, gravity, damping, dt):
    max_velocity = deck2_max_speed
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale
def limit_velocity_speedup(body, gravity, damping, dt):
    max_velocity = speedup_max_speed
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale
