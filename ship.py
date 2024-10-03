import pygame
import random
from laser import Laser
from const import HEIGHT
from item import *

class Ship:
    
    def __init__(self, x, y, vel = 1, laser_vel = 3, health=100, cooldown = 60, dmg = 10, critchance = 0, critdmg = 200) -> None:
        self.x = x
        self.y = y
        self.health = float(health)
        self.max_health = health
        self.vel = float(vel)
        self.laser_vel = laser_vel
        self.dmg = float(dmg)
        self.critchance = critchance
        self.critdmg = critdmg
        self.cooldown = cooldown
        # self.firerate = firerate
        self.ship_img = None
        self.laser_img = None
        self.lasers:list[Laser] = []
        self.cool_down_counter = 0
        self.move_counter_y = 0
        self.move_counter_x = 0
        self.items: list[Item] = []
        
    def draw(self, window:pygame.surface.Surface):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def move_lasers(self, vel, obj):
        self.cooldown_counter()
        shot = False
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= self.calcDmg()[0]
                self.lasers.remove(laser)
                shot = True
        return shot
    
    def getDmgFlat(self):
        dmg = self.dmg
        for item in self.items:
            if item.modifier == "dmg" and item.type_modifier == "add":
                dmg = item.modify(dmg)
        for item in self.items:
            if item.modifier == "dmg" and item.type_modifier == "mult":
                dmg = item.modify(dmg)
        return dmg
                
    def calcDmg(self):
        crit = False
        dmg = self.getDmgFlat()
        if random.randrange(1, 10000, 1) < self.critchance*100:
            dmg *= (self.critdmg/100)
            crit = True
        return dmg, crit
    
    def getVel(self):
        vel = self.vel
        for item in self.items:
            if item.modifier == "speed" and item.type_modifier == "add":
                vel = item.modify(vel)
        for item in self.items:
            if item.modifier == "speed" and item.type_modifier == "mult":
                vel = item.modify(vel)
        return vel
    
    def move_y(self, vel):
        if vel > 0:
            vel = self.getVel()
        else:
            vel = -self.getVel()
        self.move_counter_y %= 10
        dv = vel % 10
        vel = int(vel/10)
        if self.move_counter_y < dv:
            if vel > 0:
                self.y += (vel+1)
            else:
                self.y += (vel-1)
            self.move_counter_y += 1
        else: 
            self.y += vel
            self.move_counter_y += 1
            
    def move_x(self, vel):
        if vel > 0:
            vel = self.getVel()
        else:
            vel = -self.getVel()
        self.move_counter_x %= 10
        dv = vel % 10
        vel = int(vel/10)
        if self.move_counter_x < dv:
            if vel > 0:
                self.x += (vel+1)
            else:
                self.x += (vel-1)
            self.move_counter_x += 1
        else: 
            self.x += vel
            self.move_counter_x += 1
        
    def cooldown_counter(self):
        if self.cool_down_counter >= self.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))