import math
mu = 2
WIDTH, HEIGHT = 1920,800
#total length of sim in 242" 1920/242 = 7.9.   7.9px per inch
scale = WIDTH / 300
board_width = 3.5 * scale
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

boardqwidth = 8
   
