import pygame
import sys, os
from const import *
from func import *

def options():
    font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize'])
    run = True
    back_button = pygame.Rect(SWIDTH - SWIDTH/10 - 10, HEIGHT - HEIGHT/20 - 10, SWIDTH/10, HEIGHT/20)
    
    while run:
        try:
            bgMenu  = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (SWIDTH, HEIGHT))
            WIN.blit(bgMenu, (0, 0))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button.collidepoint(event.pos):
                                run = False
            
            draw_basic_button(back_button, 'BACK')
            pygame.display.update()
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            run = False
            
    