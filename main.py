import pygame
from func import *
from const import *
from player import Player
from enemy import Enemy
from levelupscreen import levelupscreen
from dmgclouds import DmgCloud
pygame.font.init()

def main():
    pygame.display.set_caption("Space Shooter")
    run = True
    level = 0
    main_font = pygame.font.SysFont("lucidaconsole", 30)
    lost_font = pygame.font.SysFont("comicsans", 100)
    
    enemies:list[Enemy] = []
    wave:list[str] = []
    timers:list[int] = []
    dmgclouds:list[DmgCloud] = []
    enemy_timer = 0
    
    player = Player(SWIDTH/2 - YELLOW_SPACE_SHIP.get_width()/2, HEIGHT - YELLOW_SPACE_SHIP.get_height()-20)
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0
    
    def redraw_win():
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET,0))
        # draw text
        lives_label = main_font.render(f"Lives: {player.lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        cash_label = main_font.render(f"Cash: {player.cash}", 1, (255, 255, 255))
        if player.dmg.is_integer():
            dmg_label = main_font.render(f"Damage: {int(player.dmg)}", 1, (255, 255, 255))
        else:
            dmg_label = main_font.render(f"Damage: {player.dmg}", 1, (255, 255, 255))
        critchance_label = main_font.render(f"Crit: {player.critchance}%", 1, (255, 255, 255))
        critdmg_label = main_font.render(f"Crit dmg: {player.critdmg}%", 1, (255, 255, 255))
        cooldown_label = main_font.render(f"Cooldown: {player.cooldown}", 1, (255, 255, 255))
        speed_label = main_font.render(f"Speed: {player.vel}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (SWIDTH - level_label.get_width() - 10, 10))
        WIN.blit(cash_label, (10, lives_label.get_height()+12))
        WIN.blit(dmg_label, (10, lives_label.get_height()*2+12))
        WIN.blit(critchance_label, (10, lives_label.get_height()*3+12))
        WIN.blit(critdmg_label, (10, lives_label.get_height()*4+12))
        WIN.blit(cooldown_label, (10, lives_label.get_height()*5+12))
        WIN.blit(speed_label, (10, lives_label.get_height()*6+12))
        
        for enemy in enemies:
            enemy.draw(WIN)
            
        player.draw(WIN)
        
        for dmgcloud in dmgclouds[:]:
                dmgcloud.draw(WIN)
                dmgcloud.move()
                if dmgcloud.counter == 0:
                    dmgclouds.remove(dmgcloud)
        
        if lost  == True:
            lost_label = lost_font.render("You Lost!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        try:
            redraw_win()  
            
            if player.lives <= 0 or player.health <= 0:
                lost = True 
                lost_count += 1
                
            if lost:
                if lost_count > FPS:
                    run = False
                    save(player.cash)
                else:
                    continue 
            
            if enemy_timer == 0:
                if len(timers) == 0 and len(enemies) == 0:
                    if level != 0:
                        levelupscreen(player)
                    level += 1
                    wave, timers = getEnemyWave(level)
                    enemy_timer = timers[0]
                elif len(timers) != 0:
                    enemy_timer = timers.pop(0)
                    if wave[0] != "":
                        enemies.append(spawn_enemy(wave[0], player.items))
                    wave.pop(0)
            else: enemy_timer -= 1
            
            keys = pygame.key.get_pressed()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    save(player.cash)
                    run = False
                    return "quit"
                     
            if keys[pygame.K_a] and player.x - (player.vel/10) >= 0+OFFSET: # left
                player.move_x(-player.vel)
            if keys[pygame.K_d] and player.x + (player.vel/10) + player.get_width() <= WIDTH+OFFSET: # right
                player.move_x(player.vel)
            if keys[pygame.K_w] and player.y - (player.vel/10) > 0: # up
                player.move_y(-player.vel)
            if keys[pygame.K_s] and player.y + (player.vel/10) + player.get_height() + 20 < HEIGHT: # down
                player.move_y(player.vel)
            if keys[pygame.K_SPACE]:
                player.shoot()
            if keys[pygame.K_l]:
                levelupscreen(player)
            if keys[pygame.K_m]:
                run = False
            if keys[pygame.K_0]:
                player.cash = 0
            if keys[pygame.K_9]:
                player.cash = 9999
            
            for enemy in enemies[:]:
                enemy.move_y(enemy.vel)
                if enemy.move_lasers(enemy.laser_vel, player):
                    dmgclouds.append(DmgCloud(player.x+10, player.y, enemy.dmg))
                enemy.shoot()
                
                if collide(enemy, player):
                    player.health -= enemy.health
                    dmgclouds.append(DmgCloud(enemy.x+10, enemy.y, float(enemy.health)))
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    player.lives -= 1
                    enemies.remove(enemy)
            
            playershot, shotplace, shotdmg, crit = player.move_lasers(-player.laser_vel, enemies)
            if playershot:
                dmgclouds.append(DmgCloud(shotplace[0], shotplace[1], shotdmg, crit))
        except pygame.error as error:
            save(player.cash)
            print(error)
            quit()

def main_menu():
    run = True
    title_font = pygame.font.SysFont("lucidaconsole", 50)
    pygame.display.set_mode((0,0), pygame.FULLSCREEN, display=0)
    while run:
        draw_static_bg()
        bgMenu  = pygame.transform.scale(pygame.image.load(os.path.join("spacerogue", "assets", "background-black.png")), (SWIDTH, HEIGHT))
        WIN.blit(bgMenu, (0, 0))
        title_label = title_font.render("Press SPACE to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2 + +OFFSET, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                if main() == "quit":
                    pygame.quit()
                
    pygame.quit()

main_menu()