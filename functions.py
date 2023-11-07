import pygame as py
import constants

# Returns a value clamped to minVal and maxVal
def clamp(num, minVal, maxVal):
    """
    Clamps a number between a minimum and maximum value.

    Args:
        num (int or float): The number to clamp.
        minVal (int or float): The minimum value to clamp to.
        maxVal (int or float): The maximum value to clamp to.

    Returns:
        The clamped value of `num`.
    """
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
    if player.acceleration[0] > constants.FRICTION:
        player.acceleration[0] -= constants.FRICTION
    elif player.acceleration[0] < -constants.FRICTION:
        player.acceleration[0] += constants.FRICTION  
    else:
        player.acceleration[0] = 0
    