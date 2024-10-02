from abc import ABC, abstractmethod

class Item(ABC):
    "Modifiers: add, mult, misc"
    def __init__(self, name:str, type_modifier:str) -> None:
        self.name = name
        self.type_modifier = type_modifier
        
    @abstractmethod
    def getModifiers(self):
        pass
    
    @abstractmethod
    def modify_player(self, player):
        pass
    
    @abstractmethod
    def modify_enemy(self, enemy):
        pass
        
class LuckyCoin(Item):
    "Doubles the buff from level up, but 5% chance the enemies will take it"
    def __init__(self, name = "Lucky Coin", type_modifier = "misc") -> None:
        super().__init__(name, type_modifier)
        
    def getModifiers(self):
        modifiers = []
        modifiers.append([""])
        return modifiers
    
class BetterLasers(Item):
    "+1 Damage each level"
    def __init__(self, name = "Better Lasers", type_modifier = "add") -> None:
        super().__init__(name, type_modifier)
        
    def getModifiers(self):
        return ["dmg", 1]
    
    def modify_player(self, player):
        player.dmg += 1
        
    def modify_enemy(self, enemy):
        return super().modify_enemy()