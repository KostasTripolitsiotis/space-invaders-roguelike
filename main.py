import pygame
pygame.font.init()
import os
from func import *
from const import *
from player import Player
from enemy import Enemy
from levelupscreen import levelupscreen
from dmgclouds import DmgCloud
from options import options
from hangar import hangar
from button import Button
from activeslot import ActiveSlot

def main():
    run = True
    pause = False
    pause_cooldown = 10
    level = 0
    main_font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize']-13)
    lost_font = pygame.font.SysFont("comicsans", 100)
    
    enemies:list[Enemy] = []
    wave:list[str] = []
    timers:list[int] = []
    dmgclouds:list[DmgCloud] = []
    enemy_timer = 0
    
    player = Player(SWIDTH/2 - YELLOW_SPACE_SHIP.get_width()/2, HEIGHT - YELLOW_SPACE_SHIP.get_height()-20)
    items = getSavedItems('equiped')
    remain_items = ITEMS[:]+ABILITIES[:]
    for item in items:
        levelup(item, player)
        remain_items.remove(item)
    
    try:
        slot1 = ActiveSlot(OFFSET/16, HEIGHT-OFFSET/4-OFFSET/16, player.active_items[0])
    except: slot1 = ActiveSlot(OFFSET/16, HEIGHT-OFFSET/4-OFFSET/16, None)
    try:
        slot2 = ActiveSlot(OFFSET/16*2 + OFFSET/4, HEIGHT-OFFSET/4-OFFSET/16, player.active_items[1])
    except: slot2 = ActiveSlot(OFFSET/16*2 + OFFSET/4, HEIGHT-OFFSET/4-OFFSET/16, None)
    try:
        slot3 = ActiveSlot(OFFSET/16*3 + OFFSET/2, HEIGHT-OFFSET/4-OFFSET/16, player.active_items[2])
    except: slot3 = ActiveSlot(OFFSET/16*3 + OFFSET/2, HEIGHT-OFFSET/4-OFFSET/16, None)
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0
    
    def redraw_win():
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET,0))
        
        ###  draw text for stats
        lives_label = main_font.render(f"Lives: {player.lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        if player.cash.is_integer():
            cash_label = main_font.render(f"Cash: {int(player.cash)}", 1, (255, 255, 255))
        else:
            cash_label = main_font.render(f"Cash: {player.cash}", 1, (255, 255, 255))
        if player.getDmgFlat().is_integer():
            dmg_label = main_font.render(f"Damage: {int(player.getDmgFlat())}", 1, (255, 255, 255))
        else:
            dmg_label = main_font.render(f"Damage: {round(player.getDmgFlat(), 2)}", 1, (255, 255, 255))
        critchance_label = main_font.render(f"Crit: {player.critchance}%", 1, (255, 255, 255))
        critdmg_label = main_font.render(f"Crit dmg: {player.critdmg}%", 1, (255, 255, 255))
        cooldown_label = main_font.render(f"Cooldown: {player.cooldown}", 1, (255, 255, 255))
        if player.getVel().is_integer():
            speed_label = main_font.render(f"Speed: {int(player.getVel())}", 1, (255, 255, 255))
        else:
            speed_label = main_font.render(f"Speed: {round(player.getVel(), 2)}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (SWIDTH - level_label.get_width() - 10, 10))
        WIN.blit(cash_label, (10, lives_label.get_height()+12))
        WIN.blit(dmg_label, (10, lives_label.get_height()*2+12))
        WIN.blit(critchance_label, (10, lives_label.get_height()*3+12))
        WIN.blit(critdmg_label, (10, lives_label.get_height()*4+12))
        WIN.blit(cooldown_label, (10, lives_label.get_height()*5+12))
        WIN.blit(speed_label, (10, lives_label.get_height()*6+12))
        
        ### Draw ability slots
        slot1.draw()
        slot2.draw()  
        slot3.draw()      
        
        ### Draw list of items on the right
        i = 0   
        for item in player.items+ player.active_items:
            label = main_font.render(f"{item.name}", 1, (255,255,255))
            WIN.blit(label, (SWIDTH - label.get_width() - 10, level_label.get_height()*(i+1) + 10))
            i +=1
        
        ### Draw enemies
        for enemy in enemies:
            enemy.draw(WIN)
        
        ### Draw players
        player.draw(WIN)
        
        ### Draw damage clouds
        for dmgcloud in dmgclouds[:]:
                dmgcloud.draw(WIN)
                dmgcloud.move()
                if dmgcloud.counter == 0:
                    dmgclouds.remove(dmgcloud)
        
        
        if lost  == True:
            lost_label = lost_font.render("You Lost!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (SWIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
        
        pygame.display.update()
    
    def add_to_active_slot():
        item = None
        slots = [slot1, slot2, slot3]
        sloted_items = [slot1.item, slot2.item, slot3.item]
        if level % 5 ==0 and len(player.active_items) > 0 and not(player.active_items[-1] in sloted_items):
            for i, item in enumerate(sloted_items):
                if item == None:
                    slots[i].add_item(player.active_items[-1])
                    break
                
            
        if item != None and item.type_modifier == "active":
            if slot1.item == None: slot1.item = item
            elif slot2.item == None: slot3.item = item
            elif slot3.item == None: slot3.item = item
    
    while run:
        clock.tick(FPS)
        try:
            redraw_win()  
            if pause_cooldown > 0:
                pause_cooldown -= 1
            
            if player.lives <= 0 or player.health <= 0:
                lost = True 
                lost_count += 1
                
            if lost:
                if lost_count > FPS:
                    run = False
                    save_onExit(player.cash)
                else:
                    continue 
            
            if enemy_timer == 0 and pause == False:
                if len(timers) == 0 and len(enemies) == 0:
                    levelupscreen(player, level, remain_items)
                    add_to_active_slot()
                    level += 1
                    wave, timers = getEnemyWave(level)
                    enemy_timer = timers[0]
                elif len(timers) != 0:
                    enemy_timer = timers.pop(0)
                    if wave[0] != "":
                        enemies.append(spawn_enemy(wave[0], player, level))
                    wave.pop(0)
            elif pause == False: enemy_timer -= 1
            
            keys = pygame.key.get_pressed()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    save_onExit(player.cash)
                    run = False
                    return "quit"
                        
            if keys[pygame.K_LEFT] and pause == False: # left
                if player.x - (player.getVel()/10) >= 0+OFFSET: 
                    player.move_x(-player.vel)
                else: player.x = OFFSET
            if keys[pygame.K_RIGHT] and pause == False:# right
                if player.x + (player.getVel()/10) + player.get_width() <= WIDTH+OFFSET: 
                    player.move_x(player.vel)
                else: player.x = SWIDTH - OFFSET - player.get_width()
            if keys[pygame.K_UP] and pause == False: # up
                if player.y - (player.getVel()/10) > 0: 
                    player.move_y(-player.vel)
                else: player.y = 0
            if keys[pygame.K_DOWN] and pause == False: # down
                if player.y + (player.getVel()/10) + player.get_height() + 20 < HEIGHT: 
                    player.move_y(player.vel)
                else: player.y = HEIGHT - player.get_height() - 20
            if keys[pygame.K_SPACE] and pause == False: # shot
                player.shoot()
            if keys[pygame.K_z] and pause == False: # Activate ability on slot 1
                player.useAbility(0)
            if keys[pygame.K_x] and pause == False:
                player.useAbility(1)
                
            if keys[pygame.K_l]: # go to level up screen (debug)
                levelupscreen(player, level, remain_items)
                add_to_active_slot()
            if keys[pygame.K_m]: # return to menu
                run = False
                save_onExit(player.cash)
            if keys[pygame.K_0]: # 0 cash
                player.cash = 0.0
            if keys[pygame.K_9]: # 9999 cash
                player.cash = 99999.0
            if keys[pygame.K_p]:
                if pause_cooldown <= 0:
                    pause = not(pause)
                    pause_cooldown = 10
            
            for enemy in enemies[:]: # Move/shot/check for collisions for enemies
                if pause == False:
                    enemy.move_y(enemy.vel*player.enemy_modifiers["vel"])
                    if enemy.move_lasers(player):
                        player.gotHit = True
                        dmgclouds.append(DmgCloud(player.x+10, player.y, enemy.dmg))
                    enemy.shoot()
                    
                    if collide(enemy, player):
                        CRASH.play()
                        player.gotHit = True
                        player.health -= enemy.health
                        dmgclouds.append(DmgCloud(enemy.x+10, enemy.y, float(enemy.health)))
                        enemies.remove(enemy)
                    elif enemy.y + enemy.get_height() > HEIGHT:
                        CRASH.play()
                        player.lives -= 1
                        enemies.remove(enemy)
            
            for item in player.active_items: # check for active item cooldown or active mod
                if not(item.modifier == "misc"):
                    item.update()
                else: item.update(player)
            
            if pause == False:
                playershot, shotplace, shotdmg, crit = player.move_lasers(enemies)
                if playershot:
                    dmgclouds.append(DmgCloud(shotplace[0], shotplace[1], shotdmg, crit))
        except pygame.error as error:
            save_onExit(player.cash)
            print(error)
            run = False
            pygame.quit() 

def main_menu():
    pygame.display.set_caption("Spacerogue")
    run = True
    
    OPTIONS = get_savefile()['options']
    pygame.display.set_mode(OPTIONS['res_list'][0], pygame.FULLSCREEN, display=0) 
    
    
    
    start_button = Button(SWIDTH/2 - SWIDTH/20, HEIGHT/2 - HEIGHT/20, SWIDTH/10, HEIGHT/20, name='START')
    options_button = Button(SWIDTH/2 - SWIDTH/20, start_button.y + start_button.height*1.5, SWIDTH/10, HEIGHT/20, name='OPTIONS')
    hangar_button = Button(SWIDTH/2 - SWIDTH/20, options_button.y + options_button.height*1.5, SWIDTH/10, HEIGHT/20, name='HANGAR')
    quit_button = Button(SWIDTH/2 - SWIDTH/20, hangar_button.y + hangar_button.height*1.5, SWIDTH/10, HEIGHT/20, name='QUIT')
    
    while run: 
        # try:
            bgMenu  = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (SWIDTH, HEIGHT))
            WIN.blit(bgMenu, (0, 0)) 
            start_button.draw(WIN)
            options_button.draw(WIN)
            hangar_button.draw(WIN)
            quit_button.draw(WIN)
            
            pygame.display.update()
            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if start_button.rect.collidepoint(event.pos):
                            if main() == "quit":
                                pygame.quit()
                                run = False
                        if options_button.rect.collidepoint(event.pos):
                            options()
                        if hangar_button.rect.collidepoint(event.pos):
                            hangar()
                        if quit_button.rect.collidepoint(event.pos):
                            pygame.quit()
                            run = False
            
        # except Exception:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno, exc_obj)
        #     run = False
        #     pygame.quit()
                
    pygame.quit()

main_menu()