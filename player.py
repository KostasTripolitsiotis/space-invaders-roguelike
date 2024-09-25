import pygame
from ship import Ship
from const import *
from stats import player

class Player(Ship):    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, player["vel"], player["laser_vel"], player["health"], player["cooldown"], player["dmg"])
        self.ship_img = player["spaceship_img"]
        self.laser_img = player["laser_img"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.cash = player["cash"]
        self.lives = 5
        
    def move_lasers(self, vel, objs:list[Ship]):
        kill_count = 0
        self.cooldown_counter()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.dmg
                        if obj.health <= 0:
                            self.cash += obj.worth
                            kill_count += 1
                            if obj in objs:
                                objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return kill_count
                        
    def draw(self, window:pygame.surface.Surface):
        super().draw(window)
        self.healthbar(window)
                        