import classes
allowdealer1 = classes.Debounce(.25,1)
allowdealer2 = classes.Debounce(.25,1)
allowPinch = classes.Debounce(.1, 0)
dealer_count = 4




def resetVariables():
    allowdealer1 = False
    allowdealer2 = False
    
