import classes

allowdealer1 = classes.Debounce(.25,.1)
allowdealer2 = classes.Debounce(.25,.1)
allowPinch = classes.Debounce(.1, 0)
dealer_count = 4
dealer_stop_downtime = 1
deck2full_delay = .1
deck2dealerfull_delay = .1
board_process_time = 2




def resetVariables():
    allowdealer1 = False
    allowdealer2 = False
    
