import pygame as py
import functions
import constants
import math

class Screen:
    """
    A class representing the game screen.

    Attributes:
    height (int): The height of the screen in pixels.
    width (int): The width of the screen in pixels.
    backgroundColor (tuple): The RGB color tuple representing the background color of the screen.
    window (pygame.Surface): The Pygame surface representing the game window.
    """

    def __init__(self, height, width, backgroundColor):
        self.height = height
        self.width = width
        self.backgroundColor = backgroundColor
        self.window = py.display.set_mode((width, height))

    def update(self, player, blocks):
        self.window.fill(self.backgroundColor)
        for block in blocks:
            block.draw(self)
        player.draw(self)
        py.display.update()


class Player:
    """
    A class representing a player in a game.

    Attributes:
        color (tuple): The color of the player's sprite.
        speed (float): The player's current speed.
        maxSpeed (float): The maximum speed the player can reach.
        sprite (pygame.Rect): The player's sprite.
        jumps (int): The number of times the player has jumped.
        jumpPower (float): The power of the player's jump.
        acceleration (list): The player's current acceleration in the x and y directions.
    """

    def __init__(self, height, width, x, y, jumpPower, speed, maxSpeed, playerImage):
        """
        Initializes a new instance of the Player class.

        Args:
            height (int): The height of the player's sprite.
            width (int): The width of the player's sprite.
            x (int): The x-coordinate of the player's sprite.
            y (int): The y-coordinate of the player's sprite.
            jumpPower (float): The power of the player's jump.
            speed (float): The player's current speed.
            maxSpeed (float): The maximum speed the player can reach.
            color (tuple): The color of the player's sprite.
        """
        self.moving = "right"
        self.walkAnime = 1
        self.playerImage = playerImage
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.sprite = py.Rect(x, y, width, height)
        self.jumps = 0
        self.jumpPower = jumpPower
        self.acceleration = [0, 0]
        playerSize = (50, 50)

        char1r = py.image.load("char1r.png")
        char2r = py.image.load("char2r.png")
        char3r = py.image.load("char3r.png")
        char4r = py.image.load("char4r.png")
        char1l = py.image.load("char1l.png")
        char2l = py.image.load("char2l.png")
        char3l = py.image.load("char3l.png")
        char4l = py.image.load("char4l.png")

        self.PNGDict = {"right" : [
            py.transform.scale(char1r, playerSize),
            py.transform.scale(char2r, playerSize),
            py.transform.scale(char3r, playerSize),
            py.transform.scale(char4r, playerSize)
        ],"left" : [
            py.transform.scale(char1l, playerSize),
            py.transform.scale(char2l, playerSize),
            py.transform.scale(char3l, playerSize),
            py.transform.scale(char4l, playerSize)
        ]}
        
    def move(self, buttonMap, window, blocks):
        """
        Updates the position of the sprite based on user input and game physics.

        Args:
            buttonMap (ButtonMap): An object that maps keyboard buttons to their current state.
            window (pygame.Surface): The game window surface.

        Returns:
            None
        """
        if buttonMap.map[py.K_RIGHT] and self.acceleration[0] < self.maxSpeed:
            self.acceleration[0] += self.speed
        elif buttonMap.map[py.K_LEFT] and self.acceleration[0] > -self.maxSpeed:
            self.acceleration[0] -= self.speed
        else:
            self.acceleration[0] = 0

        if buttonMap.map[py.K_SPACE] and self.jumps < 2:
            buttonMap.map[py.K_SPACE] = False
            self.acceleration[1] = -self.jumpPower
            self.jumps += 1

        self.sprite.x += self.acceleration[0]
        for block in blocks:
            if block.sprite.colliderect(self.sprite):
                if self.acceleration[0] > 0:
                    self.sprite.x = block.sprite.x - self.sprite.width
                    self.acceleration[0] = 0
                elif self.acceleration[0] < 0:
                    self.sprite.x = block.sprite.x + block.sprite.width
                    self.acceleration[0] = 0
        
        self.sprite.y += self.acceleration[1]
        for block in blocks:
            if block.sprite.colliderect(self.sprite):
                if self.acceleration[1] > 0:
                    self.sprite.y = block.sprite.y - self.sprite.height
                    self.acceleration[1] = 0
                    self.jumps = 0
                elif self.acceleration[1] < 0:
                    self.sprite.y = block.sprite.y + block.sprite.height
                    self.acceleration[1] = 0

        self.clampLocation(window)

    def draw(self, window):
        """
        Draws the player's sprite on the game window.

        Args:
            window (pygame.Surface): The game window.

        Returns:
            None
        """
        if self.acceleration[0] > 0:
            self.moving = "right"
        elif self.acceleration[0] < 0:
            self.moving = "left"   
        
        if self.acceleration[0] == 0:
            playerPNG = self.PNGDict[self.moving][0]
            
        elif self.checkGrounded(window):
            self.walkAnime += 1 / constants.PLAYER_ANIMATION_SPEED
            playerPNG = self.PNGDict[self.moving][math.floor(self.walkAnime) % 4]
            
        else:
            if self.acceleration[1] < 0:
                i = 3
            else:
                i = 1            
            playerPNG = self.PNGDict[self.moving][i]
                
             
        window.window.blit(playerPNG, (self.sprite.x, self.sprite.y))
        
    def clampLocation(self, window):
        """
        Keeps the player's sprite within the game window.

        Args:
            window (pygame.Surface): The game window.

        Returns:
            None
        """
        self.sprite.x = functions.clamp(self.sprite.x, 0, window.width - self.sprite.width)
        self.sprite.y = functions.clamp(self.sprite.y, 0, window.height - self.sprite.height)

    def checkGrounded(self, window):
        """
        Checks if the player is on the ground.

        Args:
            window (pygame.Surface): The game window.

        Returns:
            bool: True if the player is on the ground, False otherwise.
        """
        return self.sprite.y == window.height - self.sprite.height


class ButtonMap:
    """
    A class representing a mapping of keyboard buttons to their current state.

    Attributes:
        map (dict): A dictionary mapping keyboard buttons to their current state.
    """

    def __init__(self, buttons):
        """
        Initializes a new instance of the ButtonMap class.

        Args:
            buttons (list): A list of buttons to be mapped to False.
        """
        self.map = {i: False for i in buttons}

    def update(self):
        """
        Updates the state of the keyboard map based on the user's input.

        This method should be called once per frame to ensure that the keyboard map is up-to-date.

        Returns:
            None
        """
        for event in py.event.get():
            if event.type == py.QUIT:
                functions.closeGame()
            elif event.type == py.KEYDOWN and event.key in self.map:
                self.map[event.key] = True
            elif event.type == py.KEYUP and event.key in self.map:
                self.map[event.key] = False


class Block:
    def __init__(self, height, width, x, y, color, blocks):
        """
        Initializes a new instance of the Block class.

        Args:
            height (int): The height of the block in pixels.
            width (int): The width of the block in pixels.
            x (int): The x-coordinate of the block's top-left corner.
            y (int): The y-coordinate of the block's top-left corner.
            color (tuple): The RGB color tuple representing the color of the block's sprite.
            blocks (list): The list of all blocks in the game.

        Returns:
            None
        """
        self.sprite = py.Rect(x, y, width, height)
        self.color = color
        blocks.append(self)

    def draw(self, window):
        """
        Draws the sprite on the given window with the specified color.

        Args:
            window: The Pygame window to draw the sprite on.
        """
        py.draw.rect(window.window, self.color, self.sprite)