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
        
class player:
    
    def __init__(self,height,width,x,y,speed,color):
        self.color = color
        self.speed = speed
        self.sprit = py.Rect(x,y,width,height)
    
    def draw(self,window):
        py.draw.rect(window,self.color,self.sprit)
        
    def move(self,buttons):
        if buttons.map[py.K_LEFT]:
            self.sprit.x -= self.speed
        if buttons.map[py.K_RIGHT]:
            self.sprit.x += self.speed
        if buttons.map[py.K_SPACE]:
            self.sprit.y -= self.speed
            
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