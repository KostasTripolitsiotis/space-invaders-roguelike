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
    
    vel_upgrade_button = pygame.Rect(0, 0, 64, 16)
    dmg_upgrade_button = pygame.Rect(0, 0, 64, 16)
    health_upgrdade_button = pygame.Rect(0, 0, 64, 16)
    cooldown_upgrade_button = pygame.Rect(0, 0, 64, 16)
    critchance_upgrade_button = pygame.Rect(0, 0, 64, 16)
    critdmg_upgrade_button = pygame.Rect(0, 0, 64, 16)
    
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
            stats = getShipStats(selected_spaceship)
            stats_max = YELLOW_MAX
            vel_label = stats_font.render(f'Speed: {str(stats['vel'])}', 1, (255,255,255))
            laser_vel_label = stats_font.render(f'Laser Speed: {str(stats['laser_vel'])}', 1, (255,255,255))
            dmg_label = stats_font.render(f'Damage: {str(stats['dmg'])}', 1, (255,255,255))
            health_label = stats_font.render(f'Health: {str(stats['health'])}', 1, (255,255,255))
            cooldown_label = stats_font.render(f'Cooldown {str(stats['cooldown'])}', 1, (255,255,255))
            critchance_label = stats_font.render(f'Crit%: {str(stats['critchance'])}', 1, (255,255,255))
            critdmg_label = stats_font.render(f'Crit mult: {str(stats['critdmg'])}', 1, (255,255,255))
            
            # blit amount of stats
            WIN.blit(vel_label, (OFFSET+critdmg_label.get_width()-vel_label.get_width(), 13))
            WIN.blit(dmg_label, (OFFSET+critdmg_label.get_width()-dmg_label.get_width(), vel_label.get_height()*1+12))
            WIN.blit(health_label, (OFFSET+critdmg_label.get_width()-health_label.get_width(), vel_label.get_height()*2+12))
            WIN.blit(cooldown_label, (OFFSET+critdmg_label.get_width()-cooldown_label.get_width(), vel_label.get_height()*3+12))
            WIN.blit(critchance_label, (OFFSET+critdmg_label.get_width()-critchance_label.get_width(), vel_label.get_height()*4+12))
            WIN.blit(critdmg_label, (OFFSET, vel_label.get_height()*5+12))
            WIN.blit(COLOR_MAP[stats['color']][0], (OFFSET, vel_label.get_height()*6+12))
            
            # ugrade progres bar and buttons
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, 12, 150, vel_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, 12, 150*(stats['vel']/stats_max['vel']), vel_label.get_height()-1))
            vel_upgrade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, 12]
            draw_basic_button(vel_upgrade_button, 'Upgrade', fontzise=12)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*1+12, 150, dmg_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*1+12,
                                                    150*(stats['dmg']/stats_max['dmg']), dmg_label.get_height()-1))
            dmg_upgrade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, vel_label.get_height()*1+12]
            draw_basic_button(dmg_upgrade_button, 'Upgrade', fontzise=12)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*2+12, 150, health_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*2+12,
                                                 150*(stats['health']/stats_max['health']), health_label.get_height()-1))
            health_upgrdade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, vel_label.get_height()*2+12]
            draw_basic_button(health_upgrdade_button, 'Upgrade', fontzise=12)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*3+12, 150, cooldown_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*3+12,
                                                 150*(stats_max['cooldown']/stats['cooldown']), cooldown_label.get_height()-1))
            cooldown_upgrade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, vel_label.get_height()*3+12]
            draw_basic_button(cooldown_upgrade_button, 'Upgrade', fontzise=12)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*4+12, 150, critchance_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*4+12,
                                                 150*(stats['critchance']/stats_max['critchance']), critchance_label.get_height()-1))
            critchance_upgrade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, vel_label.get_height()*4+12]
            draw_basic_button(critchance_upgrade_button, 'Upgrade', fontzise=12)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*5+12, 150, critdmg_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5, vel_label.get_height()*5+12,
                                                 150*(stats['critdmg']/stats_max['critdmg']), critdmg_label.get_height()-1))
            critdmg_upgrade_button.topleft = [OFFSET+critdmg_label.get_width()+150+10, vel_label.get_height()*5+12]
            draw_basic_button(critdmg_upgrade_button, 'Upgrade', fontzise=12)
            
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