from const import *
from item import Item
from func import draw_border

class ActiveSlot():
    def __init__(self, x, y, item:Item):
        self.x = x
        self.y = y
        self.item:Item = item
        self.height = OFFSET/4
        self.width = OFFSET/4
        self.topleft = (x, y)
        self.bottomright = (x+self.width, y+self.height)
        self.rect = pygame.rect.Rect(x, y, self.width, self.height)
        self.color = (29, 27, 27)
        self.cooldown_color = (120, 108, 108)
        self.cooldown_surf = pygame.Surface((self.height, self.width))
        self.cooldown_surf.set_alpha(128)
        self.cooldown_rect = pygame.rect.Rect(0, 0, OFFSET/4, 0)
        self.label:pygame.Surface = None
        font = pygame.font.SysFont("lucidaconsole", int(OPTIONS['fontsize']/4))
        self.image:pygame.image = None
        if item != None:
            self.label = font.render(item.name, 1, C_WHITE)
        try: 
            self.img = pygame.transform.scale(item.img, (self.width, self.height))
        except: self.img = pygame.transform.scale(XMARK, (self.width, self.height))
        
    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)
        draw_border(WIN, self.topleft, self.bottomright, 2, C_WHITE)
        WIN.blit(self.img, (self.x, self.y))
        if self.item != None:
            self.cooldown_rect.height = (OFFSET/4) * (self.item.cooldown_counter/self.item.cooldown)
            WIN.blit(self.label, (self.rect.center[0]-self.label.get_width()/2, self.rect.center[1]-self.label.get_height()/2))
        self.cooldown_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.cooldown_surf, self.cooldown_color, self.cooldown_rect)
        WIN.blit(self.cooldown_surf, (self.x, self.y))
    