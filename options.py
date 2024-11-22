import pygame
import sys, os
from const import *
from func import *
from optionBox import OptionBox
from button import Button

def options():
    font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize'])
    run = True
    ###Labels
    fullscreen_label = font.render("Fullscreen", 0, C_WHITE)
    res_label = font.render("Resolution", 0, C_WHITE)
    ###Buttons
    back_button = Button(SWIDTH - SWIDTH/10 - 10, HEIGHT - HEIGHT/20 - 10, SWIDTH/10, HEIGHT/20, name="BACK")
    fullscreen_button = Button(SWIDTH - OFFSET, 100, SWIDTH/10, HEIGHT/20, img=CHECKMARK)
    ### Dropbar
    res_optionbar = OptionBox(SWIDTH - OFFSET +50, 200 - res_label.get_height(), 200, 
                              res_label.get_height(), OPTIONS['res_list'], not(fullscreen_button.clicked))
    ### TODO res (dropdown bar with pygame.display.list_modes()), volume (slider bar or dropdown), 

    def redraw_win():
        bgMenu  = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (SWIDTH, HEIGHT))
        WIN.blit(bgMenu, (0, 0))
        draw_basic_button(back_button, 'BACK')
        back_button.draw(WIN)

        ### Draw Options
        # Fullscreen
        WIN.blit(fullscreen_label, (OFFSET, 100-fullscreen_label.get_height()))
        fullscreen_button.draw(WIN)

        # Resolutions
        WIN.blit(res_label, (OFFSET, res_label.get_height()))
        res_optionbar.draw(WIN)
        
        
    while run:
        # try:
            
            keys = pygame.key.get_pressed()
            res_optionbar.update(pygame.event.get())
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button.rect.collidepoint(event.pos):
                                run = False
                        if fullscreen_button.rec.collidepoint(event.pos):
                            fullscreen_button.clicked = not(fullscreen_button.clicked)
                            pygame.display.toggle_fullscreen()
                            res_optionbar.clickable = not(res_optionbar.clickable)
            redraw_win()
            pygame.display.update()
            
        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
        #     run = False
            
    