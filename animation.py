import pygame as py
import math
import main

global playerAcceleration

kConstants['blockRadius'] = main.kConstants['blockRadius']
kConstants['playerRadius'] = main.kConstants['playerRadius']

playerSize = (kConstants['playerRadius'],kConstants['playerRadius'])

char1r = py.image.load("char1r.png")
char2r = py.image.load("char2r.png")
char3r = py.image.load("char3r.png")
char4r = py.image.load("char4r.png")
char1l = py.image.load("char1l.png")
char2l = py.image.load("char2l.png")
char3l = py.image.load("char3l.png")
char4l = py.image.load("char4l.png")

blockSize = (kConstants['blockRadius'],kConstants['blockRadius'])
blockTexture = py.image.load("block.png")

kRCADict = {
    1 : py.transform.scale(char1r, playerSize),
    2 : py.transform.scale(char2r, playerSize),
    3 : py.transform.scale(char3r, playerSize),
    4 : py.transform.scale(char4r, playerSize)
}

kLCADict = {
    1 : py.transform.scale(char1l, playerSize),
    2 : py.transform.scale(char2l, playerSize),
    3 : py.transform.scale(char3l, playerSize),
    4 : py.transform.scale(char4l, playerSize)
}
char1r = py.transform.scale(char1r, playerSize)
char2r = py.transform.scale(char2r, playerSize)
char3r = py.transform.scale(char3r, playerSize)
char4r = py.transform.scale(char4r, playerSize)
char1l = py.transform.scale(char1l, playerSize)
char2l = py.transform.scale(char2l, playerSize)
char3l = py.transform.scale(char3l, playerSize)
char4l = py.transform.scale(char4l, playerSize)

blockTexture = py.transform.scale(blockTexture,blockSize)

def animatePlayer():
    
    global walkAnime
    global moving
    global playerPNG
    
    if main.playerGrounded():
        
        animeSpeed = 8
        
        if playerAcceleration[0] > 0:
            moving = "right"
            playerPNG = kRCADict[math.ceil(walkAnime / animeSpeed)]
        elif playerAcceleration[0] < 0:
            moving = "left"
            playerPNG = kLCADict[math.ceil(walkAnime / animeSpeed)]
            
        else:  
            if moving == "right":
                playerPNG = kRCADict[1]
            else:
                playerPNG = kLCADict[1]
                
        walkAnime %= 4 * animeSpeed
        walkAnime += 1
            
    else:
        if playerAcceleration[0] > 0:
            moving = "right"
            if playerAcceleration[1] < 0:
                playerPNG = kRCADict[4]
            else:
                playerPNG = kRCADict[2]
        elif playerAcceleration[0] < 0:
            moving = "left"
            if playerAcceleration[1] < 0:
                playerPNG = kLCADict[4]
            else:
                playerPNG = kLCADict[2]
        elif moving == "right":
            if playerAcceleration[1] < 0:
                playerPNG = kRCADict[4]
            else:
                playerPNG = kRCADict[2]
        elif moving == "left":
            if playerAcceleration[1] < 0:
                playerPNG = kLCADict[4]
            else:
                playerPNG = kLCADict[2]