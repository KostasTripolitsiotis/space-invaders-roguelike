import pygame
from func import *
from const import *
from player import Player
from enemy import Enemy
from levelupscreen import levelupscreen
pygame.font.init()

def main():
    pygame.display.set_caption("Space Shooter")
    run = True
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("lucidaconsole", 30)
    lost_font = pygame.font.SysFont("comicsans", 100)
    
    enemies:list[Enemy] = []
    
    player = Player(WIDTH/2 - YELLOW_SPACE_SHIP.get_width()/2, HEIGHT - YELLOW_SPACE_SHIP.get_height()-20)
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0
    
    def redraw_win():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        cash_label = main_font.render(f"Cash: {player.cash}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(cash_label, (10, lives_label.get_height()+12))
        
        for enemy in enemies:
            enemy.draw(WIN)
            
        player.draw(WIN)
        
        if lost  == True:
            lost_label = lost_font.render("You Lost!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        try:
            redraw_win()  
            
            if lives <= 0 or player.health <= 0:
                lost = True 
                lost_count += 1
                
            if lost:
                if lost_count > FPS:
                    run = False
                    save(player.cash)
                else:
                    continue 
            
            if len(enemies) == 0:
                if level != 0:
                    levelupscreen(player)
                level += 1
                player.vel += 5   
                enemies = spawn_enemies(level)
            
            keys = pygame.key.get_pressed()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(player.cash)
                    pygame.quit()
                     
            if keys[pygame.K_a] and player.x - (player.vel/10) >= 0: # left
                player.move_x(-player.vel)
            if keys[pygame.K_d] and player.x + (player.vel/10) + player.get_width() <= WIDTH: # right
                player.move_x(player.vel)
            if keys[pygame.K_w] and player.y - (player.vel/10) > 0: # up
                player.move_y(-player.vel)
            if keys[pygame.K_s] and player.y + (player.vel/10) + player.get_height() + 20 < HEIGHT: # down
                player.move_y(player.vel)
            if keys[pygame.K_SPACE]:
                player.shoot()
            if keys[pygame.K_l]:
                levelupscreen(player)
            
            for enemy in enemies[:]:
                enemy.move_y(enemy.vel)
                enemy.move_lasers(enemy.laser_vel, player)
                enemy.shoot()
                
                if collide(enemy, player):
                    player.health -= 10
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
                    
            player.move_lasers(-player.laser_vel, enemies)
        except pygame.error as error:
            save(player.cash)
            print(error)
            quit()

def main_menu():
    run = True
    title_font = pygame.font.SysFont("lucidaconsole", 50)
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press SPACE to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                main()
                
    pygame.quit()

main_menu()