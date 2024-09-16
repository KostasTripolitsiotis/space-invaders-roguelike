import pygame
from ship import Ship
from const import *
from laser import Laser

class Enemy(Ship):
    def __init__(self, x, y, color, firerate, vel=1, laser_vel=3, health=100) -> None:
        super().__init__(x, y, vel, laser_vel, health)
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.firerate = firerate
        
    def draw(self, window:pygame.surface.Surface):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1