import classes

allowdealer1 = classes.Debounce(.25,.1)
allowdealer2 = classes.Debounce(.25,.1)
allowPinch = classes.Debounce(.1, 0)
dealer_count = 4
dealer_stop_downtime = .35
dealer_stop_downtime1 = .45
deck2full_delay = .2
deck2dealerfull_delay = .1
board_process_time = 1.7





def resetVariables():
    allowdealer1 = False
    allowdealer2 = False
    
