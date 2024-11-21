from abc import ABC, abstractmethod
from const import FPS
import random

class Item(ABC):
    """Type Modifiers: add, mult, misc, rep, active
    Modify: speed, dmg, vel, crit, crit dmg, worth, misc, laser_vel"""
    def __init__(self, name:str, type_modifier:str, modifier: str, description: str) -> None:
        self.name = name
        self.type_modifier = type_modifier
        self.modifier = modifier
        self.description = description
        self.img = None
        self.duration:int = None
        self.duration_counter:int = None
        self.cooldown:int = None
        self.cooldown_counter:int = None
        self.active:bool = None
        self.onCooldown:bool = None
        
    @abstractmethod
    def modify(self, value):
        pass
    
class LuckyCoin(Item):
    "Doubles the buff from level up, but 10% chance it will buff the enemy"
    def __init__(self, name = "Lucky Coin", type_modifier = "misc", modifier = "misc") -> None:
        super().__init__(name, type_modifier, modifier, "x2 level up bonus\n10% will affect enemies")
        pass
        
    def modify(self):
        lucky = True
        if random.randint(0, 10000) < 1000:
            lucky = False
        return lucky
    
class BetterLasers(Item):
    "+1 Damage each level"
    def __init__(self, name = "Better Lasers", type_modifier = "rep", modifier = "dmg") -> None:
        super().__init__(name, type_modifier, modifier, description="+1dmg per level")
        self.damage = 1
    
    def modify(self, obj):
        obj.dmg += self.damage
       
class JetEngine(Item):
    "+10% Speed"
    def __init__(self, name = "Jet Engine", type_modifier = "mult", modifier = "speed") -> None:
        super().__init__(name, type_modifier, modifier, "+10% speed")
        self.speed = 1.1
    
    def modify(self, speed):
        return speed * self.speed
    
class BiggerGuns(Item):
    "+10% Damage"
    def __init__(self, name = "Bigger Guns", type_modifier = "mult", modifier = "dmg") -> None:
        super().__init__(name, type_modifier, modifier, "+10% dmg")
        self.dmg = 1.1

    def modify(self, dmg):
        return dmg * self.dmg
    
class GoldenShot(Item):
    "10% more cash per spaceship"
    def __init__(self, name = "Golden Shot", type_modifier = "mult", modifier = "worth") -> None:
        super().__init__(name, type_modifier, modifier, "+10% cash")
        self.worth = 1.1

    def modify(self, worth):
        return worth * self.worth
    
class ConcentratedBeam(Item):
    "+10% laser speed, +1 pierce"
    def __init__(self, name = 'Concentrated Beam', type_modifier = 'mult', modifier = 'laser_vel') -> None:
        super().__init__(name, type_modifier, modifier, "+1 pierce")
        self.laserspeed = 1.1
        
    def modify(self, laserspeed):
        return laserspeed * self.laserspeed
    
class Multishot(Item):
    "Adds 2 more shots to your laser, 33% less damage per laser"
    def __init__(self, name = 'Multishot', type_modifier = 'mult', modifier = 'dmg') -> None:
        super().__init__(name, type_modifier, modifier, "+2 lasers")
        self.dmg = 0.66
        
    def modify(self, dmg):
        return dmg * self.dmg

class Boosters(Item):
    "+50% speed for 3sec"
    def __init__(self, name = "Boosters", type_modifier = "active", modifier = "speed", description = "+50% speed for 3sec"):
        super().__init__(name, type_modifier, modifier, description)
        
        self.vel = 1.5
        self.duration = 3*FPS
        self.duration_counter = 0
        self.cooldown = 10*FPS
        self.cooldown_counter = 0
        self.active = False
        self.onCooldown = False
    
    def activate(self):
        if self.onCooldown == False:
            self.active = True
            self.duration_counter = self.duration
            self.cooldown_counter = self.cooldown
            self.onCooldown = True
    
    def update(self):
        if self.cooldown_counter > 0: # Lower cooldown if skill has been used
            self.cooldown_counter -=1
            if self.cooldown_counter == 0:
                self.onCooldown = False

        if self.active == True:
            self.duration_counter -=1
            
            if self.duration_counter == 0:
                self.active = False
    
    def modify(self, vel):
        if self.active == True:
            return vel*self.vel
        else: return vel
        
class Freeze(Item): 
    def __init__(self, name = "Freeze", type_modifier="active", modifier="misc", description="Freeze enemies for 3 sec"):
        super().__init__(name, type_modifier, modifier, description)
        
        self.enemy_vel = 0
        self.enemy_firerate = 0
        self.duration = 3*FPS
        self.duration_counter = 0
        self.cooldown = 25*FPS
        self.cooldown_counter = 0
        self.active = False
        self.onCooldown = False
        
    def activate(self, player):
        if self.onCooldown == False:
            self.active = True
            self.duration_counter = self.duration
            self.cooldown_counter = self.cooldown
            self.onCooldown = True
            player.enemy_modifiers['vel'] *= self.enemy_vel
    
    def update(self, player):
        if self.cooldown_counter > 0: # Lower cooldown if skill has been used
            self.cooldown_counter -=1
            if self.cooldown_counter == 0:
                self.onCooldown = False

        if self.active == True:
            self.duration_counter -=1
            
            if self.duration_counter == 0:
                self.active = False
                player.enemy_modifiers['vel'] = 1
    
    def modify(self, vel):
        pass
        # if self.active == True:
        #     return vel*self.vel
        # else: return vel