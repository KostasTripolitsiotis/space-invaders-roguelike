import pygame
import random
import math
from ship import Ship
from const import *
from laser import Laser

class Enemy(Ship):
    def __init__(self, x, y, color, firerate, vel, laser_vel, health, cooldown, worth, dmg, critchance, critdmg) -> None:
        super().__init__(x, y, vel, laser_vel, health, cooldown, dmg, critchance, critdmg)
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.firerate = firerate
        self.worth = worth
        
    def draw(self, window:pygame.surface.Surface):
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        if random.randrange(0, int(self.firerate*FPS)) == 1:
            if self.cool_down_counter == 0:
                laser = Laser(self.x-15, self.y, self.laser_img, self.laser_vel)
                self.lasers.append(laser)
                self.cool_down_counter = 1
    
    def healthbar(self, window):
        width = self.ship_img.get_width()-12
        pygame.draw.rect(window, (255, 0, 0), (self.x + 6, self.y - 5, width, 5))
        pygame.draw.rect(window, (0, 255, 0), (self.x + 6, self.y - 5, math.ceil(width * (self.health/self.max_health)), 5))
        
class Blue(Enemy):
    def __init__(self, x, y, color, firerate, vel=1, laser_vel=3, health=15, cooldown=120) -> None:
        super().__init__(x, y, color, firerate, vel, laser_vel, health, cooldown)
        