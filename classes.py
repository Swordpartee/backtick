import pygame as py
import functions

class Screen:
    def __init__(self, height, width, backgroundColor):
        self.height = height
        self.width = width
        self.backgroundColor = backgroundColor
        self.window = py.display.set_mode((width, height))

    def update(self, player):
        self.window.fill(self.backgroundColor)
        player.draw(self.window)
        py.display.update()


import pygame as py
import functions

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

    def __init__(self, height, width, x, y, jumpPower, speed, maxSpeed, color):
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
        self.color = color
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.sprite = py.Rect(x, y, width, height)
        self.jumps = 0
        self.jumpPower = jumpPower
        self.acceleration = [0, 0]
        
    def move(self, buttonMap, window):
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
            
        self.sprite = self.sprite.move(self.acceleration)
        
        self.clampLocation(window)
        

    def draw(self, window):
        """
        Draws the player's sprite on the game window.

        Args:
            window (pygame.Surface): The game window.

        Returns:
            None
        """
        py.draw.rect(window, self.color, self.sprite)

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
    def __init__(self, buttons):
        self.map = {i: False for i in buttons}

    def update(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                functions.closeGame()
            elif event.type == py.KEYDOWN and event.key in self.map:
                self.map[event.key] = True
            elif event.type == py.KEYUP and event.key in self.map:
                self.map[event.key] = False
        
        