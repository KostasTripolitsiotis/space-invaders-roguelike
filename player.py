import pygame
from ship import Ship
from const import *
from stats import player
from item import *

class Player(Ship):    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, player["vel"], player["laser_vel"], player["health"], player["cooldown"], player["dmg"])
        self.ship_img = player["spaceship_img"]
        self.laser_img = player["laser_img"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.cash = player["cash"]
        self.lives = 5
        self.critchance = player["critchance"]
        self.critdmg = player["critdmg"]
        self.items: list[Item] = []
        self.items.append(BetterLasers())
        
    def move_lasers(self, vel, objs:list[Ship]):
        shot = False
        shotcoord = [0, 0]
        shotdmg = 0
        crit = False
        self.cooldown_counter()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        shot = True
                        shotcoord = [laser.x, laser.y]
                        shotdmg, crit = self.calcDmg()
                        obj.health -= shotdmg
                        if obj.health <= 0:
                            shotdmg += obj.health
                            self.cash += obj.worth
                            if obj in objs:
                                objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return shot, shotcoord, shotdmg, crit
                        
    def draw(self, window:pygame.surface.Surface):
        super().draw(window)
        self.healthbar(window)
        
    def healthbar(self, window:pygame.surface.Surface):
        font = pygame.font.SysFont("comicssans", 17)
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
        if self.health.is_integer:
            healthbar_label = font.render(f"{int(self.health)}/{self.max_health}", 1, (0, 0, 0))
        else: healthbar_label = font.render(f"{self.health}/{self.max_health}", 1, (0, 0, 0))
        window.blit(healthbar_label, healthbar_label.get_rect(center = (self.x + self.ship_img.get_width()/2, self.y + self.ship_img.get_height() + healthbar_label.get_height() + 4)))
                        