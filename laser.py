import pygame
from func import collide

class Laser:
    def __init__(self, x, y, img, vel = 3) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.vel = vel
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window:pygame.surface.Surface):
        window.blit(self.img, (self.x, self.y))
        
    def move(self, vel):
        self.y += vel
         
    def off_screen(self, height):
        return not(self.y <= height and self.y >= -35)
    
    def collision(self, obj):
        return collide(obj, self)