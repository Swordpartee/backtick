import pygame as py
import constants

# Returns a value clamped to minVal and maxVal
def clamp(num, minVal, maxVal):
    if num > maxVal:
        return(maxVal)
    elif num < minVal:
        return(minVal)
    else:
        return(num)

# Closes the game
def closeGame():
    py.quit()
    quit()

def globalUpdate(buttonMap,player,window):
    """
    Updates the player's acceleration based on gravity and friction.
    
    Args:
    buttonMap (dict): A dictionary containing the current state of the keyboard buttons.
    player (Player): An instance of the Player class representing the player.
    window (pygame.Surface): The game window surface.
    """
    
    # Update vertical acceleration based on gravity
    if not player.checkGrounded(window):
        player.acceleration[1] += constants.GRAVITY
    else:
        player.acceleration[1] = 0
        player.jumps = 0
        
    # Update horizontal acceleration based on friction
    if player.acceleration[0] > constants.Friction:
        player.acceleration[0] -= constants.Friction
    elif player.acceleration[0] < -constants.Friction:
        player.acceleration[0] += constants.Friction  
    else:
        player.acceleration[0] = 0
    
    