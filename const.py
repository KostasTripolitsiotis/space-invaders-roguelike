import pygame
import os
#from win32api import GetSystemMetrics
import ctypes

user = ctypes.windll.user32
SWIDTH = user.GetSystemMetrics(0)
OFFSET = int(SWIDTH/6)
WIDTH, HEIGHT = int(2*SWIDTH/3), user.GetSystemMetrics(1)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 120

# Load images
RED_SPACE_SHIP = pygame.transform.flip(pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png")), 0, 1)
GREEN_SPACE_SHIP = pygame.transform.flip(pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")), 0, 1)
BLUE_SPACE_SHIP = pygame.transform.flip(pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png")), 0, 1)

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Backround
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
#BG_STATIC = pygame.Rect((0, 0, SWIDTH, HEIGHT), )

OPTIONS = {
    'res' : (0,0),
    'sfx' : True,
    'fontsize': int(HEIGHT/25)
    }

COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER), 
                "yellow": (YELLOW_SPACE_SHIP, YELLOW_LASER)
    }

LEVELUP_CHOICES = ['+5 Speed', '-10% Cooldown', '+3 Damage', '+10 Health', '+1 Life', '+5% Crit', '+20% Crit Dmg']
ITEMS = ['Lucky Coin', 'Better Lasers', 'Jet Engines', 'Bigger Guns', 'Golden Shot', 'Concentrated Beam', 'Multishot']

LEVELS = {
    1: [["red", 5]],
    2: [["red", 6], ["", 3], ["green", 4]],
    3: [["red", 10], ["", 3], ["green", 5]],
    4: [["red", 3], ["", 2], ["green", 3], ["red", 4], ["", 2], ["green", 4], ["red", 5], ["", 2], ["green", 5]],
    5:[["blue", 4], ["", 3], ['red', 5], ["", 2], ["green", 5], ["", 3], ["blue", 4]]
}

YELLOW_MAX = {
    "color" : 'yellow',
    "vel" : 50,
    "laser_vel" : 15,
    "dmg" : 17,
    "health" : 200,
    "cooldown" : 45,
    "critchance" : 5,
    "critdmg" : 250
}