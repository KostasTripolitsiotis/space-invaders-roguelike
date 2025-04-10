import pygame
from ship import Ship
from const import *
from stats import player
from item import *

class Player(Ship):    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, player["vel"], -player["laser_vel"], player["health"], player["cooldown"], player["dmg"])
        self.ship_img = player["spaceship_img"]
        self.laser_img = player["laser_img"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hit_img = self.mask.copy().to_surface(setcolor=C_RED, unsetcolor=(0, 0, 0, 0))
        self.cash = float(player["cash"])
        self.lives = 5
        self.critchance = player["critchance"]
        self.critdmg = player["critdmg"]
        self.enemy_modifiers = {
            "vel" : 1, 
            "health" : 1, 
            "dmg" : 1, 
            "critchance" : 1, 
            "critdmg" : 1, 
            "cooldown" : 1, 
            "worth" : 1
        }
        self.active_items:list[Item] = []
        
    def move_lasers(self, objs:list[Ship]):
        shot = False
        shotcoord = [0, 0]
        shotdmg = 0
        crit = False
        self.cooldown_counter()
        for laser in self.lasers[:]:
            laser.move()
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        CRASH.play()
                        obj.gotHit = True
                        shot = True
                        laser.pierce -= 1
                        laser.collided_enemies.append(obj.id)
                        shotcoord = [laser.x, laser.y]
                        shotdmg, crit = self.calcDmg()
                        obj.health -= shotdmg
                        if obj.health <= 0:
                            shotdmg += obj.health
                            self.cash += self.getEnemyWorth(obj.worth)
                            if obj in objs:
                                objs.remove(obj)
                        if laser in self.lasers and laser.pierce < 0:
                            self.lasers.remove(laser)
        return shot, shotcoord, shotdmg, crit
    
    def getEnemyWorth(self, worth):
        for item in self.items:
            if item.modifier == "worth":
                worth = item.modify(worth)
        return worth
    
    def draw(self, window:pygame.surface.Surface):
        super().draw(window)
        self.healthbar(window)
        
    def shoot(self):
        multishot = False
        for item in self.items:
            if item.name == "Multishot":
                multishot = True
        if multishot == True:
            super().shootMult()
        else:
            super().shoot()
        
    def healthbar(self, window:pygame.surface.Surface):
        font = pygame.font.SysFont("comicssans", 17)
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
        if self.health.is_integer:
            healthbar_label = font.render(f"{int(self.health)}/{self.max_health}", 1, (0, 0, 0))
        else: healthbar_label = font.render(f"{self.health}/{self.max_health}", 1, (0, 0, 0))
        window.blit(healthbar_label, healthbar_label.get_rect(center = (self.x + self.ship_img.get_width()/2, self.y + self.ship_img.get_height() + healthbar_label.get_height() + 4)))

    def useAbility(self, slot):
        if (slot > len(self.active_items)-1): return None # If pressed slot is larger than active items length do nothing
        else: 
            if not(self.active_items[slot].modifier == "misc"):
                self.active_items[slot].activate()
            else: self.active_items[slot].activate(self)
    
    def getVel(self):
        vel = super().getVel()
        
        for item in self.active_items:
            if item.modifier == "speed":
                vel = item.modify(vel)
        return vel