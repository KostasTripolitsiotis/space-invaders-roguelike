import pygame
import random
from laser import Laser, DiagonalLaser
from const import *
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
        self.ship_img:pygame.surface.Surface = None
        self.laser_img = None
        self.mask:pygame.Mask = None
        self.hit_img:pygame.surface.Surface = None
        self.lasers:list[Laser] = []
        self.cool_down_counter = 0
        self.move_counter_y = 0
        self.move_counter_x = 0
        self.items: list[Item] = []
        self.id = 0
        self.laser_pierce = 0
        self.gotHit = False
        self.hitcounter_max = 4
        self.hitcounter = self.hitcounter_max

    def draw(self, window:pygame.surface.Surface):
        window.blit(self.ship_img, (self.x, self.y))
        if self.gotHit == True:
            if self.hitcounter == int(self.hitcounter_max/2):
                self.hit_img = self.mask.copy().to_surface(setcolor=C_BLACK, unsetcolor=(0, 0, 0, 0))
            WIN.blit(self.hit_img, (self.x, self.y))
            self.hitcounter -= 1
            if self.hitcounter <= 0:
                self.hit_img = self.mask.copy().to_surface(setcolor=C_WHITE, unsetcolor=(0, 0, 0, 0))
                self.hitcounter = self.hitcounter_max
                self.gotHit = False

        for laser in self.lasers:
            laser.draw(window)
            
    def move_lasers(self, obj):
        self.cooldown_counter()
        shot = False
        for laser in self.lasers[:]:
            laser.move()
            if laser.off_screen():
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
    
    def getLaserVel(self):
        laser_vel = self.laser_vel
        for item in self.items:
            if item.modifier == "laser_vel" and item.type_modifier == "add":
                laser_vel = item.modify(laser_vel)
        for item in self.items:
            if item.modifier == "laser_vel" and item.type_modifier == "mult":
                laser_vel = item.modify(laser_vel)
        return laser_vel
    
    def getLaserPierce(self):
        pierce = self.laser_pierce
        for item in self.items:
            if item.name == "Concentrated Beam":
                pierce =+ 1
        return pierce
    
    def move_y(self, vel):
        if vel > 0:
            vel = self.getVel()*YMOD
        else:
            vel = -self.getVel()*YMOD
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
            vel = self.getVel()*XMOD
        else:
            vel = -self.getVel()*XMOD
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
            laser = Laser(self.x, self.y, self.laser_img, self.getLaserVel(), self.getLaserPierce())
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def shootMult(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, self.getLaserVel(), self.getLaserPierce())
            self.lasers.append(laser)
            laser = DiagonalLaser(self.x, self.y, self.laser_img, 'right', self.getLaserVel(), self.getLaserPierce())
            self.lasers.append(laser)
            laser = DiagonalLaser(self.x, self.y, self.laser_img, 'left', self.getLaserVel(), self.getLaserPierce())
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))