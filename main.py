import math
import movement
import animation
import pygame as py

FPSCLOCK = py.time.Clock()
FPS = 60

kConstants = {
    # Define screen constants
    'screenHeight' : 700,
    'screenWidth' : 1000,

    # Define player constants
    'playerRadius' : 150,
    'playerOffset' : 0,

    'playerSpeed' : 0.3,
    'maxPlayerSpeed' : 4.5,

    'playerJumpPower' : -5,
    'playerMaxJumps' : 3,

    # Define block constants
    'blockRadius' : 25,

    # Define game constants
    'grav' : 0.35,
    'fric' : 1
}
playerOffset = kConstants['playerRadius'] * 0.22

# Define game variables
playerAcceleration = [0,0]
walkAnime = 0
moving = "right"
animationTicks = 0
blockLoc = []
blocks = []
timeshift = []

# Define colors
cRed = (255,0,0)
cOrange = (255, 100, 0)
cYellow = (255,255,0)
cGreen = (0, 128, 0)
cCyan = (0,255,255)
cBlue = (0,0,255)
cPurple = (128, 0, 128)
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
window = py.display.set_mode((kConstants['screenWidth'], kConstants['screenHeight']))

# Create player
player = py.Rect(kConstants['playerOffset'],kConstants['screenHeight'], kConstants['playerRadius'] - kConstants['playerOffset'] * 2, kConstants['playerRadius'])

class block:
    def __init__(self,x,y,size,color):
        self.x = x
        self.y = y
        self.rect = py.Rect(x,y,size,size)
        self.color = color
        self.size = size
        
    def draw(self):
        # window.blit(blockTexture,(self.x,self.y))
        
        py.draw.rect(window, self.color, self.rect)

# Returns a value clamped to minVal and maxVal
def clamp(num, minVal, maxVal):
    if num > maxVal:
        return(maxVal)
    elif num < minVal:
        return(minVal)
    else:
        return(num)
        
# Check for any updates required each game cycle                
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
    if player.y == kConstants['screenHeight'] - kConstants['playerRadius']:
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
    location[0] = kConstants['blockRadius'] * math.floor(location[0] / kConstants['blockRadius'])
    location[1] = kConstants['blockRadius'] * math.floor(location[1] / kConstants['blockRadius'])
    blockLoc.append((location[0],location[1]))
    blocks.append(block(location[0],location[1],kConstants['blockRadius'],cRed))
    
# Creates game screen
def drawScreen():
    
    # Set screen color
    window.fill(cBlack)
    
    window.blit(animation.playerPNG,(player.x - kConstants['playerOffset'], player.y))
    
    for i in blocks:
        i.draw()
    
    # Update the window
    py.display.update()


# Inits the list of blocks
def initBlocks():
    for i in blockLoc:
        blocks.append(block(i[0],i[1],kConstants['blockRadius'],cWhite))

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
        movement.calcMovement()

        movement.setPlayerPose()
        
        animation.animatePlayer()
        
        timeshift.append([(player.x, player.y),animation.playerPNG])
    
    else:
        
        movement.backInTime()
        
    reset()

    drawScreen()