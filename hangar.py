import pygame
import sys, os
from const import *
from func import *

yellow = {
    'vel' : 65,
    'laser_vel' : 5,
    'health' : 100,
    'cooldown' : 60,
    'cash' : 8821,
    'player_color' : 'yellow'
}

def getButtonsPos(shiplist:list[pygame.Surface]) -> list[tuple[int, int]]:
    pos_list:list[tuple[int, int]] = []
    for i in range(len(shiplist)):
            if i == 0:
                pos_list.append((OFFSET/2 - shiplist[i].get_width()/2, 50))
                
            else:
                pos_list.append((OFFSET/2 - shiplist[i].get_width()/2, (shiplist[i-1].get_height() + 50)*i + 50))
    return pos_list

def hangar():
    font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize'])
    stats_font = pygame.font.SysFont("lucidaconsole", int(OPTIONS['fontsize']/2))
    run = True
    back_button = pygame.Rect(WIDTH - WIDTH/10 + OFFSET - 10, HEIGHT - HEIGHT/20 - 10, WIDTH/10, HEIGHT/20)
    ship_list:list[pygame.Surface] = [YELLOW_SPACE_SHIP, GREEN_SPACE_SHIP, RED_SPACE_SHIP, BLUE_SPACE_SHIP]
    buttons:dict[pygame.Rect] = {}
    buttons_pos:list[tuple[int, int]] = getButtonsPos(ship_list)
    selected_spaceship = 'yellow'
    
    for i in range(len(ship_list)):
        buttons[ship_list[i]] = pygame.Rect(buttons_pos[i], (ship_list[i].get_width(), ship_list[i].get_height()))
    
    def redraw_win():
        try:
            draw_static_bg()
            WIN.blit(BG, (0+OFFSET,0))
            
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET-1, 0, 1, HEIGHT))
            pygame.draw.rect(WIN, (255, 255, 255), (SWIDTH-OFFSET, 0, 1, HEIGHT))
            
            # Draw spaceship left of screen
            for i in range(len(ship_list)):
                if i == 0:
                    draw_basic_button(buttons[ship_list[i]], "")
                    WIN.blit(ship_list[i], (OFFSET/2 - ship_list[i].get_width()/2, 50))
                    
                else:
                    WIN.blit(ship_list[i], (OFFSET/2 - ship_list[i].get_width()/2, (ship_list[i-1].get_height() + 50)*i + 50))
            
            # Grab stats from selected spaceship     
            stats = getActiceSpaceship(selected_spaceship)
            vel_label = stats_font.render(str(stats['vel']), 1, (255,255,255))
            laser_vel_label = stats_font.render(str(stats['laser_vel']), 1, (255,255,255))
            dmg_label = stats_font.render(str(stats['dmg']), 1, (255,255,255))
            health_label = stats_font.render(str(stats['health']), 1, (255,255,255))
            cooldown_label = stats_font.render(str(stats['cooldown']), 1, (255,255,255))
            critchance_label = stats_font.render(str(stats['critchance']), 1, (255,255,255))
            critdmg_label = stats_font.render(str(stats['critdmg']), 1, (255,255,255))
            
            WIN.blit(vel_label, (OFFSET, 12))
            WIN.blit(laser_vel_label, (OFFSET, vel_label.get_height()+12))
            WIN.blit(dmg_label, (OFFSET, vel_label.get_height()*2+12))
            WIN.blit(health_label, (OFFSET, vel_label.get_height()*3+12))
            WIN.blit(cooldown_label, (OFFSET, vel_label.get_height()*4+12))
            WIN.blit(critchance_label, (OFFSET, vel_label.get_height()*5+12))
            WIN.blit(critdmg_label, (OFFSET, vel_label.get_height()*6+12))
            WIN.blit(COLOR_MAP[stats['color']][0], (OFFSET, vel_label.get_height()*7+12))
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
    
    while run:
        try:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button.collidepoint(event.pos):
                            run = False
                        if buttons[YELLOW_SPACE_SHIP].collidepoint(event.pos):
                            selected_spaceship = 'yellow' 
            
            redraw_win()
            draw_basic_button(back_button, 'BACK')
            pygame.display.update()
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
            run = False