import math
import pygame as py
import random
import time

FPSCLOCK = py.time.Clock()
FPS = 60

# Define screen constants
kScreenHeight = 700
kScreenWidth = 1000

# Define player constants
kPlayerRadius = 50

kPlayerSpeed = 0.3
kMaxPlayerSpeed = 4.5

kPlayerJumpPower = -5
kPlayerMaxJumps = 3


# Define block constants
kBlockRadius = 25
blockLoc = [(0,0),(500,675),(500,650),(525,675),(525,650)]
blocks = []

# Define game constants
kGrav = 0.35
kFric = 1

# Define game variables
playerAcceleration = [0,0]
walkAnime = 0
moving = "right"
animationTicks = 0
jumps = 0

# Define colors
cBlack = (0,0,0)
cWhite = (255,255,255)
cBlue = (0,0,255)
cRed = (255,0,0)

# Create button mappings
buttonMap = {
    py.K_LEFT : False,
    py.K_RIGHT : False,
    py.K_SPACE : False,
    py.K_DOWN : False,
    py.K_LALT : False,
    py.K_LSHIFT : False
}

# Create game screen
window = py.display.set_mode((kScreenWidth, kScreenHeight))

# Create player
player = py.Rect(0,kScreenHeight, kPlayerRadius, kPlayerRadius)

playerSize = (kPlayerRadius,kPlayerRadius)
char1r = py.image.load("char1r.png")
char2r = py.image.load("char2r.png")
char3r = py.image.load("char3r.png")
char4r = py.image.load("char4r.png")
char1l = py.image.load("char1l.png")
char2l = py.image.load("char2l.png")
char3l = py.image.load("char3l.png")
char4l = py.image.load("char4l.png")
blockSize = (kBlockRadius,kBlockRadius)
blockTexture = py.image.load("block.png")

char1r = py.transform.scale(char1r, playerSize)
char2r = py.transform.scale(char2r, playerSize)
char3r = py.transform.scale(char3r, playerSize)
char4r = py.transform.scale(char4r, playerSize)
char1l = py.transform.scale(char1l, playerSize)
char2l = py.transform.scale(char2l, playerSize)
char3l = py.transform.scale(char3l, playerSize)
char4l = py.transform.scale(char4l, playerSize)
blockTexture = py.transform.scale(blockTexture,blockSize)

class block:
    def __init__(self,x,y,size,color):
        self.x = x
        self.y = y
        self.rect = py.Rect(x,y,size,size)
        self.color = color
        self.size = size
        
    def draw(self):
        # window.blit(blockTexture,(self.x,self.y))
        
        py.draw.rect(window, cWhite, self.rect)

# Returns a value clamped to minVal and maxVal
def clamp(num, minVal, maxVal):
    if num > maxVal:
        return(maxVal)
    elif num < minVal:
        return(minVal)
    else:
        return(num)

# Calls functions to alculate player movement every game tick
def calcMovement():
        
    move()
            
    jump()
        
    applyGrav()
    
    applyFric()

# If holding l/r, move
def move():
    if abs(playerAcceleration[0]) < kMaxPlayerSpeed:
        if buttonMap[py.K_LEFT]:
            playerAcceleration[0] -= kPlayerSpeed
        if buttonMap[py.K_RIGHT]:
            playerAcceleration[0] += kPlayerSpeed
                
# If the player pressed space, jump
def jump():
    
    global jumps
    
    if buttonMap[py.K_SPACE] and jumps < kPlayerMaxJumps:
        jumps = jumps + 1
        buttonMap[py.K_SPACE] = False
        playerAcceleration[1] = kPlayerJumpPower

# Applies gravity to the player
def applyGrav():
    if not playerGrounded():
        playerAcceleration[1] += kGrav

# Applies friction to the player
def applyFric():
    if playerGrounded:
        if not ((buttonMap[py.K_LEFT] and playerAcceleration[0] < 0 and not buttonMap[py.K_RIGHT]) or (buttonMap[py.K_RIGHT] and playerAcceleration[0] > 0 and not buttonMap[py.K_LEFT])):
            if playerAcceleration[0] > 0:
                playerAcceleration[0] -= kFric
                if playerAcceleration[0] < 0:
                    playerAcceleration[0] = 0
            elif playerAcceleration[0] < 0:
                playerAcceleration[0] += kFric
                if playerAcceleration[0] > 0:
                    playerAcceleration[0] = 0
        
# Check for any resets required each game cycle                
def reset():
    
    global jumps
    global animationTicks
    
    if playerGrounded():
        jumps = 0
    
    animationTicks += 1
    
    playerAcceleration[0] = math.floor(playerAcceleration[0] * 10) * 0.1
    playerAcceleration[1] = math.floor(playerAcceleration[1] * 10) * 0.1
    
# Checks if the player is standing on the ground, or on a block
def playerGrounded():
    if player.y == kScreenHeight - kPlayerRadius:
        return(True)
    else:
        player.y += 1 
        if player.collidelist(blocks) != -1:
            player.y -= 1 
            return(True)
        else:
            player.y -= 1 
            return(False)

# Gets button mapping        
def getButtons():
    for event in py.event.get():
        # if quit, quit
        if event.type == py.QUIT:
            py.quit()
            quit()
            
        # If player presses a key, set button map to true
        if event.type == py.KEYDOWN:
            if event.key in buttonMap:
                buttonMap[event.key] = True
        
        # If player stops pressing a key, set button map to false
        if event.type == py.KEYUP:
            if event.key in buttonMap:
                buttonMap[event.key] = False

# Moves player pose based on acceleration
def setPlayerPose():
    
    # Stop player movement if they are on the edge of the screen
    if (playerGrounded() and playerAcceleration[1] > 0) or (player.y == 0 and playerAcceleration[1] < 0):
        playerAcceleration[1] = 0
    if (playerAcceleration[0] < 0 and player.x == 0) or (playerAcceleration[0] > 0 and player.x == kScreenWidth - kPlayerRadius):
        playerAcceleration[0] = 0
    
    # Move player pose
    player.x += playerAcceleration[0] * (kPlayerRadius/100)
    
    if isColliding():
        collisionBlock = blocks[player.collidelist(blocks)]
        if playerAcceleration[0] > 0:
            player.x = collisionBlock.x - kPlayerRadius
            playerAcceleration[0] = 0
        elif playerAcceleration[0] < 0:
            player.x = collisionBlock.x + collisionBlock.size
            playerAcceleration[0] = 0
    
    player.y += playerAcceleration[1] * (kPlayerRadius/100)
    if isColliding():
        collisionBlock = blocks[player.collidelist(blocks)]
        if playerAcceleration[1] > 0:
            player.y = collisionBlock.y - kPlayerRadius
            playerAcceleration[1] = 0
        elif playerAcceleration[1] < 0:
            player.y = collisionBlock.y + collisionBlock.size
            playerAcceleration[1] = 0
                
    player.y = clamp(player.y,0,kScreenHeight - kPlayerRadius)
    player.x = clamp(player.x,0,kScreenWidth - kPlayerRadius)

# Creates game screen
def drawScreen():
    
    # Set screen color
    window.fill(cBlack)
    
    # Draw player
    animatePlayer()
    
    for i in blocks:
        i.draw()
    
    # Update the window
    py.display.update()

def animatePlayer():
    
    global walkAnime
    global moving
    
    if playerGrounded():
        if playerAcceleration[0] > 0:
            moving = "right"
            if walkAnime == 0:
                window.blit(char1r,(player.x,player.y))
            elif walkAnime == 1:
                window.blit(char2r,(player.x,player.y))
            elif walkAnime == 2:
                window.blit(char3r,(player.x,player.y))
            elif walkAnime == 3:
                window.blit(char4r,(player.x,player.y))
        elif playerAcceleration[0] < 0:
            moving = "left"
            if walkAnime == 0:
                window.blit(char1l,(player.x,player.y))
            elif walkAnime == 1:
                window.blit(char2l,(player.x,player.y))
            elif walkAnime == 2:
                window.blit(char3l,(player.x,player.y))
            elif walkAnime == 3:
                window.blit(char4l,(player.x,player.y))
        elif moving == "right":
            window.blit(char1r,(player.x,player.y))
        elif moving == "left":
            window.blit(char1l,(player.x,player.y))
        if playerGrounded():
            if animationTicks % 5 == 0:
                walkAnime += 1
                walkAnime %= 4
    else:
        if playerAcceleration[0] > 0:
            moving = "right"
            if playerAcceleration[1] < 0:
                window.blit(char4r,(player.x,player.y))
            else:
                window.blit(char2r,(player.x,player.y))
        elif playerAcceleration[0] < 0:
            moving = "left"
            if playerAcceleration[1] < 0:
                window.blit(char4l,(player.x,player.y))
            else:
                window.blit(char2l,(player.x,player.y))
        elif moving == "right":
            if playerAcceleration[1] < 0:
                window.blit(char4r,(player.x,player.y))
            else:
                window.blit(char2r,(player.x,player.y))
        elif moving == "left":
            if playerAcceleration[1] < 0:
                window.blit(char4l,(player.x,player.y))
            else:
                window.blit(char2l,(player.x,player.y))

# Inits the list of blocks
def initBlocks():
    for i in blockLoc:
        blocks.append(block(i[0],i[1],kBlockRadius,cWhite))

# Checks if the player is colliding with a block
def isColliding():
    if player.collidelist(blocks) != -1:
        return(True)
    else:
        return(False)
    
initBlocks()

# Game loop
while True:
    FPSCLOCK.tick(FPS)
    
    getButtons()

    calcMovement()

    setPlayerPose()
    
    reset()

    drawScreen()