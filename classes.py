import pygame as py
import functions

class screen: 
    
    # Define the data for our screen
    def __init__(self, height, width, backroundColor):
        self.height = height
        self.width = width
        self.backroundColor = backroundColor
        self.window = py.display.set_mode((width,height))
        
    def update(self,player):
        
        self.window.fill(self.backroundColor)
        
        player.draw(self.window)
        
        py.display.update()
        
class playerAcceleration:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

class player:

    def __init__(self,height,width,x,y,speed,speedCap,friction,jumpPower,maxJumps,color):
        self.color = color
        self.speed = speed
        self.speedCap = speedCap
        self.friction = friction
        self.jumps = 0
        self.jumped = False
        self.jumpPower = jumpPower
        self.maxJumps = maxJumps
        self.acceleration = playerAcceleration(0,0)
        self.sprit = py.Rect(x,y,width,height)
    
    def draw(self,window):
        py.draw.rect(window,self.color,self.sprit)
        
    def move(self,buttonMap):
        
        if self.acceleration.x < self.speedCap and self.acceleration.x > -self.speedCap:
            if buttonMap.map[py.K_LEFT]:
                self.acceleration.x -= self.speed
            if buttonMap.map[py.K_RIGHT]:
                self.acceleration.x += self.speed
                
        print(self.acceleration.x)
                
        if not ((buttonMap.map[py.K_LEFT] and self.acceleration.x <= 0) or (buttonMap.map[py.K_RIGHT] and self.acceleration.x >= 0)):
            if self.acceleration.x > self.friction:
                self.acceleration.x -= self.friction
            elif self.acceleration.x < -self.friction:
                self.acceleration.x += self.friction
            else:
                self.acceleration.x = 0
            
        self.jump(buttonMap)
        
        self.sprit.x += self.acceleration.x
        self.sprit.y += self.acceleration.y
            
    def jump(self,buttonMap):
        if self.jumped:
            if buttonMap[py.K_SPACE] and self.jumps < self.MaxJumps:
                self.acceleration.y = self.jumpPower
                self.jumps += 1
                self.jumped = True
        elif not buttonMap.map[py.K_SPACE]:
            self.jumped = False
            
    def checkGrounded(self,window):
        if self.sprit.y == window.height - self.sprit.height:
            return (True)
        else:
            return (False)
        
class buttonMap:
    
    def __init__(self,buttons):
        self.map = {}
        for i in buttons:
            self.map[i] = False
            
    def update(self):
        for i in py.event.get():
            if i.type == py.QUIT:
                functions.closeGame()
                
            elif i.type == py.KEYDOWN and i.key in self.map:
                self.map[i.key] = True
            
            elif i.type == py.KEYUP and i.key in self.map:
                self.map[i.key] = False