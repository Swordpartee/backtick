import main
import pygame as py

global playerAcceleration
global buttonMap
global kMaxPlayerSpeed
global kPlayerMaxJumps
global kPlayerSpeed
global kPlayerJumpPower
global kGrav
global kFric
global jumps
global player
global kPlayerRadius
global kPlayerOffset
global blocks
global kScreenHeight
global kScreenWidth
global timeshift

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
    
    if buttonMap[py.K_SPACE] and jumps < kPlayerMaxJumps:
        jumps = jumps + 1
        buttonMap[py.K_SPACE] = False
        playerAcceleration[1] = kPlayerJumpPower

# Applies gravity to the player
def applyGrav():
    if not main.playerGrounded():
        playerAcceleration[1] += kGrav

# Applies friction to the player
def applyFric():
    if main.playerGrounded:
        if not ((buttonMap[py.K_LEFT] and playerAcceleration[0] < 0 and not buttonMap[py.K_RIGHT]) or (buttonMap[py.K_RIGHT] and playerAcceleration[0] > 0 and not buttonMap[py.K_LEFT])):
            if playerAcceleration[0] > 0:
                playerAcceleration[0] -= kFric
                if playerAcceleration[0] < 0:
                    playerAcceleration[0] = 0
            elif playerAcceleration[0] < 0:
                playerAcceleration[0] += kFric
                if playerAcceleration[0] > 0:
                    playerAcceleration[0] = 0
                    
# Moves player pose based on acceleration
def setPlayerPose():
    
    # Stop player movement if they are on the edge of the screen
    if (main.playerGrounded() and playerAcceleration[1] > 0) or (player.y == 0 and playerAcceleration[1] < 0):
        playerAcceleration[1] = 0
    if (playerAcceleration[0] < 0 and player.x == 0) or (playerAcceleration[0] > 0 and player.x == kScreenWidth - (kPlayerRadius - kPlayerOffset * 2)):
        playerAcceleration[0] = 0
    
    # Move player pose
    player.x += playerAcceleration[0] * ((kPlayerRadius - kPlayerOffset * 2)/100)
    if main.isColliding():
        collisionBlock = blocks[player.collidelist(blocks)]
        if playerAcceleration[0] > 0:
            player.x = collisionBlock.x - (kPlayerRadius - kPlayerOffset * 2)
            playerAcceleration[0] = 0
        elif playerAcceleration[0] <= 0:
            player.x = collisionBlock.x + collisionBlock.size
            playerAcceleration[0] = 0
    
    player.y += playerAcceleration[1] * (kPlayerRadius/100)
    if main.isColliding():
        collisionBlock = blocks[player.collidelist(blocks)]
        if playerAcceleration[1] > 0:
            player.y = collisionBlock.y - kPlayerRadius
            playerAcceleration[1] = 0
        elif playerAcceleration[1] < 0:
            player.y = collisionBlock.y + collisionBlock.size
            playerAcceleration[1] = 0
                
    player.y = main.clamp(player.y,0,kScreenHeight - kPlayerRadius)
    player.x = main.clamp(player.x,0,kScreenWidth - (kPlayerRadius - kPlayerOffset * 2))
    
def backInTime():
    global playerPNG 
    
    if not len(timeshift) == 0:
        player.x = timeshift[-1][0][0]
        player.y = timeshift[-1][0][1]
        playerPNG = timeshift[-1][1]
        timeshift.pop(-1)
