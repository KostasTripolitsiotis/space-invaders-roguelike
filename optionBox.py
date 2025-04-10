import pygame
from const import *
font = pygame.font.SysFont("lucidaconsole", int(OPTIONS['fontsize']/2))

class OptionBox():
  
    def __init__(self, x, y, w, h, option_list, clickable, color=C_WHITE, highlight_color=C_WHITE, disabled_color=C_WHITE, font=font, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.disabled_color = disabled_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.clickable = clickable
        self.active_option = -1

    def draw(self, surf):
        color = self.highlight_color if self.menu_active else self.color if self.clickable else self.disabled_color
        pygame.draw.rect(surf, color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(str(self.option_list[self.selected]), 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                text = str(text)
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos) and self.clickable
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1
    
    def get_height(self):
        return self.rect.height
    def get_width(self):
        return self.rect.width
    def get_x(self):
        return self.rect.x
    def get_y(self):
        return self.rect.y