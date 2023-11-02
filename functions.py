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
    
    if buttonMap.map[py.K_LEFT]:
        player.sprit.x -= player.speed
    if buttonMap.map[py.K_RIGHT]:
        player.sprit.x += player.speed
    
    if not player.checkGrounded(window):
        player.sprit.y += 1
    
    player.sprit.y = clamp(player.sprit.y,0,window.height - player.sprit.height)
    player.sprit.x = clamp(player.sprit.x,0,window.width - player.sprit.width)
    
    