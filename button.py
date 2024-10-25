import pygame
from func import *
from const import *

class Button():
    def __init__(self, x:int, y:int, width:int, height:int, *, label:str = "", img:pygame.Surface = None, 
                 border:bool = True, border_thic:int = 1, border_color:tuple[int, int, int] = (255, 255, 255), 
                 border_thic_active:int = 3, border_color_active:tuple[int, int, int] = (100, 100, 100),
                 clicked:bool = False, fontsize:int = OPTIONS['fontsize'], color:tuple[int, int, int] = (29, 27, 27)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.fontsize = fontsize
        self.img = img
        self.border = border
        self.border_thic = border_thic
        self.border_color = border_color
        self.border_thic_active = border_thic_active
        self.border_color_active  = border_color_active
        self.clicked = clicked
        self.color = color
        
    def draw(self, surface:pygame.Surface):
        temp_color = self.color
        mod = 2
        if self.clicked == True:
            r, g, b = int(self.color[0]*mod), int(self.color[1]*mod), int(self.color[2]*mod)
            temp_color = (r, g, b)
        draw_basic_button(self.rect, self.label, self.fontsize, self.border_thic, self.border_color, temp_color)
        if self.img != None:
            surface.blit(self.img, (self.x, self.y))
            
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            draw_border(surface, (self.x, self.y), (self.x+self.width, self.y+self.height), self.border_thic_active, self.border_color_active)
            
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        