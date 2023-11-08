# Description: This is the main file for the game. It contains the main game loop and initializes the game window and player objects.

import pygame as py
import functions
import classes
import constants 

# Initialize FPS clock
FPSClock = py.time.Clock()

blocks = []

# Initialize our game window and5 player objects
window = classes.Screen(constants.SCREEN_HEIGHT, constants.SCREEN_WIDTH, constants.C_BLACK)
player = classes.Player(constants.K_PLAYER_SIZE, constants.K_PLAYER_SIZE, 0, 0, constants.JUMP_POWER, constants.PLAYER_SPEED, constants.PLAYER_MAX_SPEED, constants.C_RED)
buttonMap = classes.ButtonMap([py.K_LEFT, py.K_RIGHT, py.K_SPACE])

deltaList = []

while True:
    # Limit the game to 240 FPS
    delatTime = FPSClock.tick(constants.FPS) / 4.8
    deltaList.append(delatTime)
    i = 0
    deltaAverage = 0
    for delta in deltaList:
        i += 1
        deltaAverage += delta
    deltaAverage /= i
    print(deltaAverage)
    
    # Update the state of the keyboard buttons
    buttonMap.update()
    
    # Update the player's acceleration and check for collisions
    functions.globalUpdate(buttonMap, player, window)
    
    # Move the player
    player.move(buttonMap, window, blocks, delatTime)
    
    # Draw the player and update the display
    window.update(player, blocks, buttonMap)
