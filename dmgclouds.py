from const import *
from func import *

class DmgCloud():
    def __init__(self, x:int, y:int, label:float, crit:bool = False, counter = 30) -> None:
        self.x = x
        self.y = y
        self.crit = crit
        self.font = pygame.font.SysFont("lucidaconsole", 20)
        self.label = self.getLabel(label)
        self.counter = 30
        
    def move(self):
        self.y -= 1
        self.counter -= 1
        
    def draw(self, window):
        window.blit(self.label, (self.x, self.y))
    
    def getLabel(self, label:float):
        if label.is_integer():
            label = int(label)
        else:
            label = round(label, 2)
        if self.crit == False:
            return self.font.render(str(label), 1, (250, 253, 247))
        else:
            return self.font.render(str(label), 1, (255, 0, 0))