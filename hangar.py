import pygame
import sys, os
from const import *
from func import *
from button import Button
import itertools

def getItemButtonPos(items:list[str]) -> list[tuple[int, int]]:
    pos_list:list[tuple[int, int]] = []
    for i in range(len(items)):
        if i == 0:
            pos_list.append((SWIDTH-OFFSET+OFFSET/2-OFFSET/4-25, OFFSET/4))
        else:
            pos_list.append((SWIDTH-OFFSET+OFFSET/2-OFFSET/4-25, 110*i+OFFSET/4))
    return pos_list

def getAbilityButtonPos(items:list[str]) -> list[tuple[int, int]]:
    pos_list:list[tuple[int, int]] = getItemButtonPos(items)
    return_list:list[tuple[int, int]] = []
    for pos in pos_list:
        return_list.append((pos[0] + OFFSET/3 + OFFSET/12, pos[1]))
    return return_list

def hangar():
    item_font = pygame.font.SysFont("lucidaconsole", int(OPTIONS['fontsize']/2))
    title_font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize']*2)
    stats_font = pygame.font.SysFont("lucidaconsole", int(OPTIONS['fontsize']))
    title_label = title_font.render("HANGAR", 1, (255, 255, 255))
    run = True
    back_btn = Button(WIDTH - WIDTH/10 + OFFSET - 10, HEIGHT - HEIGHT/20 - 10, WIDTH/10, HEIGHT/20, name='BACK')
    selected_spaceship = 'yellow'
    selected_stats = getShipStats(selected_spaceship)
    cash_label = stats_font.render("Cash: " + str(int(get_savefile()['cash'])), 1, C_WHITE)
    
    # Upgrade buttons
    vel_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("vel")), fontsize=stats_font.get_linesize())
    dmg_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("dmg")), fontsize=stats_font.get_linesize())
    health_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("health")), fontsize=stats_font.get_linesize())
    cooldown_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("cooldown")), fontsize=stats_font.get_linesize())
    critchance_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("critchance")), fontsize=stats_font.get_linesize())
    critdmg_upgrade_btn = Button(0, 0, stats_font.get_linesize()*4, stats_font.get_linesize()-1, name=str(get_upgrade_cost("critdmg")), fontsize=stats_font.get_linesize())
    upgrade_buttons = [(vel_upgrade_btn, "vel"), (dmg_upgrade_btn, "dmg"), (health_upgrade_btn, "health"), 
                       (cooldown_upgrade_btn, "cooldown"), (critchance_upgrade_btn, "critchance"), (critdmg_upgrade_btn, "critdmg")]
    
    ### Perk Buttons
    #item_list
    item_buttons:list[Button] = []
    item_buttons_pos:list[tuple[int, int]] = getItemButtonPos(ITEMS)
    for i in range(len(ITEMS)):
        try:
            item_buttons.append(Button(item_buttons_pos[i][0], item_buttons_pos[i][1], OFFSET/4, OFFSET/4, name=ITEMS[i], fontsize=item_font.get_linesize(), img=ITEMS_PNG[i]))
        except:
            item_buttons.append(Button(item_buttons_pos[i][0], item_buttons_pos[i][1], OFFSET/4, OFFSET/4, name=ITEMS[i], fontsize=item_font.get_linesize()))

    #ability list
    ability_buttons:list[Button] = []
    ability_button_pos:list[tuple[int, int]] = getAbilityButtonPos(ABILITIES)
    for i in range(len(ABILITIES)):
        try:
            ability_buttons.append(Button(ability_button_pos[i][0], ability_button_pos[i][1], OFFSET/4, OFFSET/4, name=ABILITIES[i], fontsize=item_font.get_linesize(), img=ABILITIES_PNG[i]))
        except:
            ability_buttons.append(Button(ability_button_pos[i][0], ability_button_pos[i][1], OFFSET/4, OFFSET/4, name=ABILITIES[i], fontsize=item_font.get_linesize()))

    ### Equiped items
    equiped_items = getSavedItems('equiped')
    for button in itertools.chain(item_buttons, ability_buttons): 
        if button.name in equiped_items: button.clicked = True

    ### Locked items
    unlocked_items = getSavedItems('unlocked')
    for button in itertools.chain(item_buttons, ability_buttons):
        if not(button.name in unlocked_items): button.isClickable = False
        
    cash_buttons:list[tuple[Button, str]] = []
    for button in itertools.chain(item_buttons, ability_buttons):
        if button.isClickable == False:
            cash_buttons.append((Button(button.x, button.y, button.width, button.height, name=str(get_item_cost(button.name)), fontsize=stats_font.get_linesize()), button.name))
    
    def redraw_win():
        try:
            draw_static_bg()
            WIN.blit(BG, (0+OFFSET,0))
            WIN.blit(title_label, (SWIDTH/2-title_label.get_width()/2, title_label.get_height()))       
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET-1, 0, 1, HEIGHT))
            pygame.draw.rect(WIN, (255, 255, 255), (SWIDTH-OFFSET, 0, 1, HEIGHT))
            back_btn.draw(WIN)
            WIN.blit(cash_label, (OFFSET/2-cash_label.get_width()/2, 10))
            
            # Stats labels 
            stats_max = MAX_STATS
            vel_label = stats_font.render(f'Speed: {str(selected_stats["vel"])}', 1, (255,255,255))
            laser_vel_label = stats_font.render(f'Laser Speed: {str(selected_stats["laser_vel"])}', 1, (255,255,255))
            dmg_label = stats_font.render(f'Damage: {str(selected_stats["dmg"])}', 1, (255,255,255))
            health_label = stats_font.render(f'Health: {str(selected_stats["health"])}', 1, (255,255,255))
            cooldown_label = stats_font.render(f'Cooldown {str(selected_stats["cooldown"])}', 1, (255,255,255))
            critchance_label = stats_font.render(f'Crit%: {str(selected_stats["critchance"])}', 1, (255,255,255))
            critdmg_label = stats_font.render(f'Crit mult: {str(selected_stats["critdmg"])}', 1, (255,255,255))
            
            bar_width = 300
            padx = (WIDTH-critdmg_label.get_width()-bar_width-stats_font.get_linesize()-1)/4
            pady = HEIGHT/4 - (vel_label.get_height()*6)/4
            padx_button = 15
            
            # blit selected spaceship
            img_scale = 3/2
            spaceship_image = pygame.transform.scale(COLOR_MAP[selected_stats['color']][0], 
                                                     (COLOR_MAP[selected_stats['color']][0].get_width()*img_scale, 
                                                      COLOR_MAP[selected_stats['color']][0].get_height()*img_scale))
            WIN.blit(spaceship_image, (SWIDTH/2 - spaceship_image.get_width()/2, 
                                                    HEIGHT-spaceship_image.get_height()/2-pady))
            
            # blit amount of stats
            WIN.blit(vel_label, (OFFSET+critdmg_label.get_width()-vel_label.get_width()+padx, 12+pady))
            WIN.blit(dmg_label, (OFFSET+critdmg_label.get_width()-dmg_label.get_width()+padx, vel_label.get_height()*1+12+pady))
            WIN.blit(health_label, (OFFSET+critdmg_label.get_width()-health_label.get_width()+padx, vel_label.get_height()*2+12+pady))
            WIN.blit(cooldown_label, (OFFSET+critdmg_label.get_width()-cooldown_label.get_width()+padx, vel_label.get_height()*3+12+pady))
            WIN.blit(critchance_label, (OFFSET+critdmg_label.get_width()-critchance_label.get_width()+padx, vel_label.get_height()*4+12+pady))
            WIN.blit(critdmg_label, (OFFSET+padx, vel_label.get_height()*5+12+pady))
            
            ### blit ugrade progres bar and button 
            # Speed          
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, 12+pady, bar_width, vel_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, 12+pady, bar_width*(selected_stats['vel']/stats_max['vel']), vel_label.get_height()-1))
            vel_upgrade_btn.x, vel_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, 12+pady
            vel_upgrade_btn.updateRect()
            vel_upgrade_btn.draw(WIN)
            
            # Damage
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*1+12+pady, bar_width, dmg_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*1+12+pady,
                                                    bar_width*(selected_stats['dmg']/stats_max['dmg']), dmg_label.get_height()-1))
            dmg_upgrade_btn.x, dmg_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, vel_label.get_height()*1+12+pady
            dmg_upgrade_btn.updateRect()
            dmg_upgrade_btn.draw(WIN)
            
            # Health
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*2+12+pady, bar_width, health_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*2+12+pady,
                                                 bar_width*(selected_stats['health']/stats_max['health']), health_label.get_height()-1))
            health_upgrade_btn.x, health_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, vel_label.get_height()*2+12+pady
            health_upgrade_btn.updateRect()
            health_upgrade_btn.draw(WIN)
            
            # Cooldown
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*3+12+pady, bar_width, cooldown_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*3+12+pady,
                                                 bar_width*(stats_max['cooldown']/selected_stats['cooldown']), cooldown_label.get_height()-1))
            cooldown_upgrade_btn.x, cooldown_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, vel_label.get_height()*3+12+pady
            cooldown_upgrade_btn.updateRect()
            cooldown_upgrade_btn.draw(WIN)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*4+12+pady, bar_width, critchance_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*4+12+pady,
                                                 bar_width*(selected_stats['critchance']/stats_max['critchance']), critchance_label.get_height()-1))
            critchance_upgrade_btn.x, critchance_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, vel_label.get_height()*4+12+pady
            critchance_upgrade_btn.updateRect()
            critchance_upgrade_btn.draw(WIN)
            
            pygame.draw.rect(WIN, (70, 70, 70), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*5+12+pady, bar_width, critdmg_label.get_height()-1))
            pygame.draw.rect(WIN, (255, 255, 255), (OFFSET+critdmg_label.get_width()+5+padx, vel_label.get_height()*5+12+pady,
                                                 bar_width*(selected_stats['critdmg']/stats_max['critdmg']), critdmg_label.get_height()-1))
            critdmg_upgrade_btn.x, critdmg_upgrade_btn.y = OFFSET+critdmg_label.get_width()+bar_width+padx_button+padx, vel_label.get_height()*5+12+pady
            critdmg_upgrade_btn.updateRect()
            critdmg_upgrade_btn.draw(WIN)
            
            ### blit perks left of screen
            # Items, Abilities
            for button in item_buttons:
                button.draw(WIN)

            # Abilities
            for button in ability_buttons:
                button.draw(WIN)
                
            # Cash buttons to unlock items/abilities
            for button in cash_buttons:
                # print(button[1])
                button[0].draw(WIN)
            
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
                if keys[pygame.K_r]: # Reset spaceship stats to original
                    selected_stats = resetYellow()
                # 'L' to lock all items
                if keys[pygame.K_l]:
                    for item in unlocked_items:
                        editItems(item, 'lock') #TODO add lock/unlock func
                # 'U' to unlock all items
                if keys[pygame.K_u]:
                    for item in itertools.chain(ITEMS, ABILITIES):
                        editItems(item, 'unlock') #TODO add lock/unlock func
                    
                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouseclick
                    if event.button == 1:
                        if back_btn.rect.collidepoint(event.pos):
                            run = False
                                    
                        for button in upgrade_buttons: # Check all upgrade buttons
                            if button[0].rect.collidepoint(event.pos):
                                stat = upgrade(selected_spaceship, button[1])
                                button[0].setLabel(str(get_upgrade_cost(button[1])))
                                cash_label = stats_font.render("Cash: " + str(int(get_savefile()['cash'])), 1, C_WHITE)
                                if stat != None:
                                    selected_stats[button[1]] = stat
                                
                        for button in itertools.chain(item_buttons, ability_buttons): # Check all items
                            if button.rect.collidepoint(event.pos) and button.isClickable:
                                button.clicked = not(button.clicked) # Stay selected/de-selected
                                if button.clicked == True:
                                    editItems(button.name, 'add') # Add or remove selected item from player
                                else: editItems(button.name, 'rm')
                            
                        for button in cash_buttons[:]: # check buttons to unlock items
                            if button[0].rect.collidepoint(event.pos):
                                button[0].clicked = unlockItem(button[1])
                                if button[0].clicked == True:
                                    cash_buttons.remove(button)
                                    
                                    for item in itertools.chain(item_buttons, ability_buttons):
                                        if item.name == button[1]:
                                            item.isClickable = True
            
            redraw_win()
            pygame.display.update()
            
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, exc_obj)
            run = False
