import random
import pygame
from func import *
from const import *
from button import Button
from player import Player
from enemy import Enemy

def levelupscreen(player, level, remaining_items):
    run = True
    main_font = pygame.font.SysFont("lucidaconsole", 12)
    choice_type:str
    if level % 5 ==0:
        choices = remaining_items
        choice_type = "item"
    else:
        choices = LEVELUP_CHOICES[:]
        choice_type = "stat"
    
    choice1 = random.choice(choices)
    choices.remove(choice1)
    if choice_type == "stat":
        choice1_btn = Button((SWIDTH/2 - 50) - 200, HEIGHT/2 - 50, 100, 100, name=choice1, fontsize=main_font.get_linesize())
    else: 
        try:
            choice1_btn = Button((SWIDTH/2 - 50) - 100, HEIGHT/2 - 50, 100, 100, name=choice1, fontsize=main_font.get_linesize(), img=ITEM_TO_PNG[choice1])
        except:
            choice1_btn = Button((SWIDTH/2 - 50) - 100, HEIGHT/2 - 50, 100, 100, name=choice1, fontsize=main_font.get_linesize())
    
    choice2 = random.choice(choices)
    choices.remove(choice2)
    if choice_type == "stat":
        choice2_btn = Button(SWIDTH/2 - 50, HEIGHT/2 - 50, 100, 100, name=choice2, fontsize=main_font.get_linesize())
    else: 
        try:
            choice2_btn = Button((SWIDTH/2 - 50) + 100, HEIGHT/2 - 50, 100, 100, name=choice2, fontsize=main_font.get_linesize(), img=ITEM_TO_PNG[choice2])
        except:
            choice2_btn = Button((SWIDTH/2 - 50) + 100, HEIGHT/2 - 50, 100, 100, name=choice2, fontsize=main_font.get_linesize())
    
    if choice_type == "stat":
        choice3 = random.choice(choices)
        choices.remove(choice3)
        choice3_btn = Button((SWIDTH/2 - 50) + 200, HEIGHT/2 - 50, 100, 100, name=choice3, fontsize=main_font.get_linesize())
    
    while(run):
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET, 0))
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if choice1_btn.rect.collidepoint(event.pos):
                        levelup(choice1, player)
                        run = False
                    if choice2_btn.rect.collidepoint(event.pos):
                        levelup(choice2, player)
                        run = False
                    if choice_type == "stat" and choice3_btn.rect.collidepoint(event.pos):
                        levelup(choice3, player)
                        run = False
        
        # Draw the button on the screen
        choice1_btn.draw(WIN)
        choice2_btn.draw(WIN)
        if choice_type == "stat":
            choice3_btn.draw(WIN)
                
        pygame.display.update()