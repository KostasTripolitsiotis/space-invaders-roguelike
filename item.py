from abc import ABC, abstractmethod
import random

class Item(ABC):
    """Type Modifiers: add, mult, misc, rep
    Modify: speed, dmg, vel, crit, crit dmg, worth, misc, laser_vel"""
    def __init__(self, name:str, type_modifier:str, modifier: str) -> None:
        self.name = name
        self.type_modifier = type_modifier
        self.modifier = modifier
        
    @abstractmethod
    def getModifiers(self):
        pass
    
    @abstractmethod
    def modify_player(self, player):
        pass
    
    @abstractmethod
    def modify_enemy(self, enemy):
        pass
        
    @abstractmethod
    def modify(self, value):
        pass
    
class LuckyCoin(Item):
    "Doubles the buff from level up, but 10% chance it will buff the enemy"
    def __init__(self, name = "Lucky Coin", type_modifier = "misc", modifier = "misc") -> None:
        super().__init__(name, type_modifier, modifier)
        
    def getModifiers(self):
        modifiers = []
        modifiers.append([""])
        return modifiers
    
    def modify_player(self, player):
        pass
    
    def modify_enemy(self, enemy):
        pass
        
    def modify(self):
        lucky = True
        if random.randint(0, 10000) < 1000:
            lucky = False
        return lucky
    
class BetterLasers(Item):
    "+1 Damage each level"
    def __init__(self, name = "Better Lasers", type_modifier = "rep", modifier = "dmg") -> None:
        super().__init__(name, type_modifier, modifier)
        self.damage = 1
        
    def getModifiers(self):
        return [self.type_modifier, self.modifier, self.damage]
    
    def modify_player(self, player):
        return super().modify_player(player)
        
    def modify_enemy(self, enemy):
        return super().modify_enemy(enemy)
    
    def modify(self, obj):
        obj.dmg += self.damage
       
class JetEngine(Item):
    "+10% Speed"
    def __init__(self, name = "Jet Engine", type_modifier = "mult", modifier = "speed") -> None:
        super().__init__(name, type_modifier, modifier)
        self.speed = 1.1
        
    def getModifiers(self):
        return ["speed", "mult", self.speed]
    
    def modify_player(self, player):
        return super().modify_player(player)
        
    def modify_enemy(self, enemy):
        return super().modify_enemy(enemy)
    
    def modify(self, speed):
        return speed * self.speed
    
class BiggerGuns(Item):
    "+10% Damage"
    def __init__(self, name = "Bigger Guns", type_modifier = "mult", modifier = "dmg") -> None:
        super().__init__(name, type_modifier, modifier)
        self.dmg = 1.1
        
    def getModifiers(self):
        return ["dmg", "mult", self.dmg]

    def modify_player(self, player):
        pass

    def modify_enemy(self, enemy):
        pass

    def modify(self, dmg):
        return dmg * self.dmg
    
class GoldenShot(Item):
    "10% more cash per spaceship"
    def __init__(self, name = "Golden Shot", type_modifier = "mult", modifier = "worth") -> None:
        super().__init__(name, type_modifier, modifier)
        self.worth = 1.1
        
    def getModifiers(self):
        return ["worth", "mult", 1.1]

    def modify_player(self, player):
        pass

    def modify_enemy(self, enemy):
        pass

    def modify(self, worth):
        return worth * self.worth
    
class ConcentratedBeam(Item):
    "+10% laser speed, +1 pierce"
    def __init__(self, name = 'Concentrated Beam', type_modifier = 'mult', modifier = 'laser_vel') -> None:
        super().__init__(name, type_modifier, modifier)
        self.laserspeed = 1.1
        
    def getModifiers(self):
        pass

    def modify_player(self, player):
        pass

    def modify_enemy(self, enemy):
        pass
        
    def modify(self, laserspeed):
        return laserspeed * self.laserspeed
    
class Multishot(Item):
    "Adds 2 more shots to your laser, 33% less damage per laser"
    def __init__(self, name = 'Multishot', type_modifier = 'mult', modifier = 'dmg') -> None:
        super().__init__(name, type_modifier, modifier)
        self.dmg = 0.66
        
    def getModifiers(self):
        pass

    def modify_player(self, player):
        pass

    def modify_enemy(self, enemy):
        pass
        
    def modify(self, dmg):
        return dmg * self.dmg