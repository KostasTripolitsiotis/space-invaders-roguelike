import pygame
import sys, os
from const import *
from func import *

def hangar():
    font = pygame.font.SysFont("lucidaconsole", 40)
    run = True
    back_button = pygame.Rect(WIDTH - WIDTH/10 + OFFSET - 10, HEIGHT - HEIGHT/20 - 10, WIDTH/10, HEIGHT/20)
    
    def draw_buttons(back_button:pygame.Rect):
        pygame.draw.rect(WIN, (29, 27, 27), back_button)
        back_label = font.render("BACK", 1, (238, 240, 240))
        WIN.blit(back_label, (back_button.x + (back_button.width - back_label.get_width())/2, back_button.y + (back_button.height - back_label.get_height())/2))
        draw_border(WIN, (back_button.x, back_button.y), (back_button.x+back_button.width, back_button.y+back_button.height), 1, (255, 255, 255))
    
        pygame.display.update()
    
    def redraw_win():
        draw_static_bg()
        WIN.blit(BG, (0+OFFSET,0))
    
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
            draw_buttons(back_button)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            run = False