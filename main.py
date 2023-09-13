import math
import pygame as py

FPSCLOCK = py.time.Clock()
FPS = 60

# Define screen constants
kScreenHeight = 700
kScreenWidth = 1000

# Define player constants
kPlayerRadius = 150
kPlayerOffset = 33

kPlayerSpeed = 0.3
kMaxPlayerSpeed = 4.5

kPlayerJumpPower = -5
kPlayerMaxJumps = 3

# Define block constants
kBlockRadius = 26
blockLoc = []
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

timeshift = []

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
player = py.Rect(kPlayerOffset,kScreenHeight, kPlayerRadius - kPlayerOffset * 2, kPlayerRadius)

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
    
    if buttonMap[py.K_SPACE] and jumps <= kPlayerMaxJumps:
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
            print(stripList(blockLoc))
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
                
        if event.type == py.MOUSEBUTTONDOWN:
                spawnblock()
                
def stripList(startlist):
    stripedListed = []
    for i in startlist:
        if i not in stripedListed:
            stripedListed.append(i)
    
    return(stripedListed)

def spawnblock():
    loc = py.mouse.get_pos()
    location = [loc[0],loc[1]]
    location[0] = kBlockRadius * math.floor(location[0] / kBlockRadius)
    location[1] = kBlockRadius * math.floor(location[1] / kBlockRadius)
    blockLoc.append((location[0],location[1]))
    blocks.append(block(location[0],location[1],kBlockRadius,cWhite))

# Moves player pose based on acceleration
def setPlayerPose():
    
    # Stop player movement if they are on the edge of the screen
    if (playerGrounded() and playerAcceleration[1] > 0) or (player.y == 0 and playerAcceleration[1] < 0):
        playerAcceleration[1] = 0
    if (playerAcceleration[0] < 0 and player.x == 0) or (playerAcceleration[0] > 0 and player.x == kScreenWidth - (kPlayerRadius - kPlayerOffset * 2)):
        playerAcceleration[0] = 0
    
    # Move player pose
    player.x += playerAcceleration[0] * ((kPlayerRadius - kPlayerOffset * 2)/100)
    if isColliding():
        collisionBlock = blocks[player.collidelist(blocks)]
        if playerAcceleration[0] > 0:
            player.x = collisionBlock.x - (kPlayerRadius - kPlayerOffset * 2)
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
    player.x = clamp(player.x,0,kScreenWidth - (kPlayerRadius - kPlayerOffset * 2))
    
def backInTime():
    i = 1
    if len(timeshift) > 100:
        while i < 100:
            timeRev(i)
            i += 1
    else:
        while i < len(timeshift):
            timeRev(i)
            i += 1

def timeRev(i):
    player.x = timeshift[-i][0][0]
    player.y = timeshift[-i][0][1]

# Creates game screen
def drawScreen():
    
    # Set screen color
    window.fill(cBlack)
    
    window.blit(playerPNG,(player.x - kPlayerOffset, player.y))
    
    timeshift.append([(player.x - kPlayerOffset, player.y),playerPNG])
    
    if len(timeshift) > 100:
        timeshift.pop(0)
    
    for i in blocks:
        i.draw()
    
    # Update the window
    py.display.update()

def animatePlayer():
    
    global walkAnime
    global moving
    global playerPNG
    
    if playerGrounded():
        
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
                playerPNG = char4r
            else:
                playerPNG = char2r
        elif playerAcceleration[0] < 0:
            moving = "left"
            if playerAcceleration[1] < 0:
                playerPNG = char4l
            else:
                playerPNG = char2l
        elif moving == "right":
            if playerAcceleration[1] < 0:
                playerPNG = char4r
            else:
                playerPNG = char2r
        elif moving == "left":
            if playerAcceleration[1] < 0:
                playerPNG = char4l
            else:
                playerPNG = char2l

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

    if not buttonMap[py.K_LSHIFT]:
        calcMovement()

        setPlayerPose()
        
        animatePlayer()
    
    else:
        
        backInTime()
        
    reset()

    drawScreen()
