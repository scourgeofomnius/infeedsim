import math
mu = .3
WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
board_width = 5.5 * scale
board_height = 1.5 * scale
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
grey = (110,110,110)
red = (255,0,0)
yellow = (252,228,13)



tc_height = 200
tc_width = 70 * scale

decline_angle = 180 + 10
decline_length = 150*scale
decline_start_y = tc_height
decline_end_y = (1*(int((decline_length/scale)*math.sin(decline_angle)))) + tc_height
decline_start_x = tc_width
decline_end_x = decline_length + tc_width

declinestop_start_y = decline_end_y - 20
declinestop_end_y = declinestop_start_y
declinestop_start_x = decline_end_x - 50
declinestop_end_x = declinestop_start_x + 35

deck2dealer_start_x = decline_end_x
deck2dealer_start_y = decline_end_y
deck2dealer_end_x = deck2dealer_start_x + int((0 * scale))
deck2dealer_end_y = deck2dealer_start_y

deck2_end_x = deck2dealer_end_x + int((45*scale))
deck2_start_y = deck2dealer_end_y
deck2_start_x = deck2dealer_end_x
deck2_end_y = deck2_start_y

speedup_position = tc_width - (18 * scale)
dealer2_position = deck2_end_x - (45 * scale)

boardqwidth = 14
   

WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
mu = 2
objects = []

dealer_count = 4
dealer_stop_downtime = .25
dealer_stop_uptime = .01
dealer_stop_downtime1 = .35
deck2full_delay = .2
deck2dealerfull_delay = .01
board_process_time = 3.7

#64 /48 =1.3 gives the scale. this was taken from a time measurement across deck2
speed_scale = 1.4
tc_max_speed = 70 * speed_scale
tc2_max_speed = 120 * speed_scale
deck2_max_speed = 100 * speed_scale
decline_max_speed = 100 * speed_scale
speedup_max_speed = 200
