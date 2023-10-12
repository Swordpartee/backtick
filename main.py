import pygame as py
import functions
import classes

FPSClock = py.time.Clock()
FPS = 60

window = classes.screen(700,1000,(0,0,0))
player = classes.player(100,100,200,200,0.3,9,0.8,4,-3,(255,255,255))
buttonMap = classes.buttonMap([py.K_LEFT,py.K_RIGHT,py.K_SPACE])

while True:
    
    # Tick our clock to contine the loop
    FPSClock.tick(FPS)
    
    buttonMap.update()
    
    functions.globalUpdate(buttonMap,player,window)
    
    # Call our window update function to update the screen
    window.update(player)