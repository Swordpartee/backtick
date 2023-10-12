import pygame as py

# Returns a value clamped to minVal and maxVal
def clamp(num, minVal, maxVal):
    if num > maxVal:
        return(maxVal)
    elif num < minVal:
        return(minVal)
    else:
        return(num)

def closeGame():
    py.quit()
    quit()
    
def globalUpdate(buttonMap,player,window):
    player.move(buttonMap)