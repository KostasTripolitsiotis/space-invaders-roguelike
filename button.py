import pygame
from const import C_WHITE, OPTIONS
from func import *
from const import *
from func import C_WHITE, OPTIONS

class Button():
    def __init__(self, x:int, y:int, width:int, height:int, *, name:str = "", img:pygame.Surface = None, 
                 border:bool = True, border_thic:int = 1, border_color:tuple[int, int, int] = C_WHITE, 
                 border_thic_active:int = 3, border_color_active:tuple[int, int, int] = (100, 100, 100),
                 clicked:bool = False, fontsize:int = OPTIONS['fontsize'], color:tuple[int, int, int] = (29, 27, 27)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        font = pygame.font.SysFont("lucidaconsole", fontsize)
        self.label = font.render(name, 1, C_WHITE)
        self.fontsize = fontsize
        self.img = img
        if self.img != None:
            self.img = pygame.transform.scale(self.img, (width, height))
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
        
        if self.img != None:
            draw_basic_button(self.rect, "", self.fontsize, self.border_thic, self.border_color, temp_color)
            surface.blit(self.img, (self.x, self.y))
        else:
            draw_basic_button(self.rect, self.name, self.fontsize, self.border_thic, self.border_color, temp_color)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            draw_border(surface, (self.x, self.y), (self.x+self.width, self.y+self.height), self.border_thic_active, self.border_color_active)
            if self.img != None:
                surface.blit(self.label, (mouse_pos[0], mouse_pos[1]-15))
            
            
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class CheckButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, *, name: str = "", img: pygame.Surface = None, 
                 border: bool = True, border_thic: int = 1, border_color: tuple[int, int, int] = C_WHITE, 
                 border_thic_active: int = 3, border_color_active: tuple[int, int, int] = (100, 100, 100), 
                 clicked: bool = False, fontsize: int = OPTIONS['fontsize'], color: tuple[int, int, int] = (29, 27, 27)):
        super().__init__(x, y, width, height, name=name, img=img, border=border, border_thic=border_thic, 
                         border_color=border_color, border_thic_active=border_thic_active, 
                         border_color_active=border_color_active, clicked=clicked, fontsize=fontsize, color=color)
        
    def draw(self, surface:pygame.Surface):
        temp_color = self.color
        mod = 2
        if self.clicked == True:
            r, g, b = int(self.color[0]*mod), int(self.color[1]*mod), int(self.color[2]*mod)
            temp_color = (r, g, b)
        
        if self.img != None and self.clicked == True:
            draw_basic_button(self.rect, "", self.fontsize, self.border_thic, self.border_color, temp_color)
            surface.blit(self.img, (self.x, self.y))
        else:
            draw_basic_button(self.rect, "", self.fontsize, self.border_thic, self.border_color, temp_color)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            draw_border(surface, (self.x, self.y), (self.x+self.width, self.y+self.height), self.border_thic_active, self.border_color_active)
            if self.img != None:
                surface.blit(self.label, (mouse_pos[0], mouse_pos[1]-15))