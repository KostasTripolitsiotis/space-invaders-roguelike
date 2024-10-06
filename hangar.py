import pygame
import sys, os
from const import *
from func import *

def getButtonsPos(shiplist:list[pygame.Surface]) -> list[tuple[int, int]]:
    pass

def hangar():
    font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize'])
    run = True
    back_button = pygame.Rect(WIDTH - WIDTH/10 + OFFSET - 10, HEIGHT - HEIGHT/20 - 10, WIDTH/10, HEIGHT/20)
    ship_list:list[pygame.Surface] = [YELLOW_SPACE_SHIP, GREEN_SPACE_SHIP, RED_SPACE_SHIP, BLUE_SPACE_SHIP]
    buttons:list[pygame.Rect] = []
    buttons_pos:list[tuple[int, int]] = []
    
    def redraw_win():
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET,0))
        
        pygame.draw.rect(WIN, (255, 255, 255), (OFFSET-1, 0, 1, HEIGHT))
        pygame.draw.rect(WIN, (255, 255, 255), (SWIDTH-OFFSET, 0, 1, HEIGHT))
        
        # Draw spaceship left of screen
        for i in range(len(ship_list)):
            if i == 0:
                WIN.blit(ship_list[i], (OFFSET/2 - ship_list[i].get_width()/2, 50))
                button = ship_list[i].get_rect(x=ship_list[i].get_abs_offset[0], y=ship_list[i].get_abs_offset[1])
                
            else:
                WIN.blit(ship_list[i], (OFFSET/2 - ship_list[i].get_width()/2, (ship_list[i-1].get_height() + 50)*i + 50))
    
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
            
            redraw_win()
            draw_basic_button(back_button, 'BACK')
            pygame.display.update()
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            run = False