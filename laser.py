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
        
    def move(self):
        self.y += self.vel
         
    def off_screen(self):
        from const import OFFSET, WIDTH, HEIGHT
        return not(self.y <= HEIGHT and self.y >= -35) or not(self.x > OFFSET - 50 and self.x < WIDTH + OFFSET - 50)
    
    def collision(self, obj):
        return collide(obj, self)
    
class DiagonalLaser(Laser):
    def __init__(self, x, y, img, vel=3, direction = 'right') -> None:
        super().__init__(x, y, img, vel)
        self.direction = direction
        self.vel_x = vel/3
        
    def move (self):
        self.y += self.vel
        if self.direction == 'right':
            self.x += self.vel_x
        else: self.x -= self.vel_x