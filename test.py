

['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 
 'consolas', 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 
 'georgia', 'impact', 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 
 'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 
 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 
 'microsoftyibaiti', 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 
 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript', 
 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 'simsun', 
 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner', 'sylfaen', 
 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 
 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight', 'holomdl2assets', 'cascadiacoderegular', 'cascadiamonoregular']

# bahnschrift
# impact
# lucidaconsole
# 
# 
import shelve
from func import getActiceSpaceship
import pygame
pygame.font.init()

yellow = {
    "color" : 'yellow',
    # "spaceship_img" : YELLOW_SPACE_SHIP, 
    # "laser_img" : YELLOW_LASER, 
    "vel" : 20,
    "laser_vel" : 15,
    "dmg" : 10,
    "health" : 100,
    "cooldown" : 60,
    "critchance" : 0,
    "critdmg" : 200
}
def open_savefile() -> list:
    with shelve.open('savefile/test') as f:
        for item in f:
            print(f'{item} = {f[item]}')
            
def save(cash: int) -> None:
    with shelve.open('savefile/test') as f:
        f['yellow'] = yellow
        f['cash'] = cash
        f['color'] = 'yellow'

cash = 50
# save(50)
open_savefile()
stats = getActiceSpaceship('yellow')

print(stats)