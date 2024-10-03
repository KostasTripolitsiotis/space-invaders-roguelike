import random
import pygame
from func import *
from const import *
from player import Player
from enemy import Enemy

def levelupscreen(player, level):
    run = True
    main_font = pygame.font.SysFont("lucidaconsole", 15)
    if level % 5 ==0:
        choices = ITEMS[:]
    else:
        choices = LEVELUP_CHOICES[:]
    
    choice1 = random.choice(choices)
    choices.remove(choice1)
    choice1_surface = pygame.Surface((100, 100))
    choice1_label = main_font.render(choice1, 1, (238, 240, 240))
    choice1_rect = choice1_label.get_rect(center=(choice1_surface.get_width()/2, choice1_surface.get_height()/2))
    choice1_btn_rect = pygame.Rect((WIN.get_width()/2 - choice1_surface.get_width()/2) - 200, WIN.get_height()/2 - choice1_surface.get_height()/2, 100, 100)
    
    choice2 = random.choice(choices)
    choices.remove(choice2)
    choice2_surface = pygame.Surface((100, 100))
    choice2_label = main_font.render(choice2, 1, (238, 240, 240))
    choice2_rect = choice2_label.get_rect(center=(choice2_surface.get_width()/2, choice2_surface.get_height()/2))
    choice2_btn_rect = pygame.Rect(WIN.get_width()/2 - choice2_surface.get_width()/2, WIN.get_height()/2 - choice2_surface.get_height()/2, 100, 100)
    
    choice3 = random.choice(choices)
    choices.remove(choice3)
    choice3_surface = pygame.Surface((100, 100))
    choice3_label = main_font.render(choice3, 1, (238, 240, 240))
    choice3_rect = choice3_label.get_rect(center=(choice3_surface.get_width()/2, choice3_surface.get_height()/2))
    choice3_btn_rect = pygame.Rect((WIN.get_width()/2 - choice3_surface.get_width()/2) + 200, WIN.get_height()/2 - choice3_surface.get_height()/2, 100, 100)
    
    while(run):
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET, 0))
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if choice1_btn_rect.collidepoint(event.pos):
                    levelup(choice1, player)
                    run = False
                if choice2_btn_rect.collidepoint(event.pos):
                    levelup(choice2, player)
                    run = False
                if choice3_btn_rect.collidepoint(event.pos):
                    levelup(choice3, player)
                    run = False
                
        # Check if the mouse is over the button. This will create the button hover effect
        if choice1_btn_rect.collidepoint(pygame.mouse.get_pos()):
            draw_border(choice1_surface, 2, 2)
        else:
            pygame.draw.rect(choice1_surface, (19, 17, 17), (0, 0, 100, 100))
            
        if choice2_btn_rect.collidepoint(pygame.mouse.get_pos()):
            draw_border(choice2_surface, 2, 2)
        else:
            pygame.draw.rect(choice2_surface, (19, 17, 17), (0, 0, 100, 100))
            
        if choice3_btn_rect.collidepoint(pygame.mouse.get_pos()):
            draw_border(choice3_surface, 2, 2)
        else:
            pygame.draw.rect(choice3_surface, (19, 17, 17), (0, 0, 100, 100))
        
        # Show the button text    
        choice1_surface.blit(choice1_label, choice1_rect)
        choice2_surface.blit(choice2_label, choice2_rect)
        choice3_surface.blit(choice3_label, choice3_rect)
        
        # Draw the button on the screen
        WIN.blit(choice1_surface, (choice1_btn_rect.x, choice1_btn_rect.y))
        WIN.blit(choice2_surface, (choice2_btn_rect.x, choice2_btn_rect.y))
        WIN.blit(choice3_surface, (choice3_btn_rect.x, choice3_btn_rect.y))
                
        pygame.display.update()