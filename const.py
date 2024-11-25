import pygame
import os
#from win32api import GetSystemMetrics
import ctypes

user = ctypes.windll.user32
SWIDTH = user.GetSystemMetrics(0)
OFFSET = int(SWIDTH/6)
WIDTH, HEIGHT = int(2*SWIDTH/3), user.GetSystemMetrics(1)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
XMOD = SWIDTH/1920
YMOD = HEIGHT/1080

# Colors
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_BLUEVIOLET = (138, 43, 226)
C_BACKROUND = (55, 53, 59)
C_RED = (255, 90, 90)

### Load images
# Enemy ships
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

# Misc
CHECKMARK = pygame.image.load(os.path.join("assets", "checkmark.png"))
XMARK = pygame.image.load(os.path.join("assets", "xmark.png"))

OPTIONS = {
    'res' : (0,0),
    'res_list': pygame.display.list_modes(),
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

### Items
ITEMS = ['Lucky Coin', 'Better Lasers', 'Jet Engines', 'Bigger Guns', 'Golden Shot', 'Concentrated Beam', 'Multishot'] #, 'Boosters', 'Freeze'
ABILITIES = ['Boosters', 'Freeze']
# Items PNG
LUCKY_COIN = pygame.image.load(os.path.join("assets", "golden coin.png"))
MULTISHOT = pygame.image.load(os.path.join("assets", "multishot.png"))
BETTER_LASERS = pygame.image.load(os.path.join("assets", "better_lasers.png"))
JET_ENGINES = pygame.image.load(os.path.join("assets", "jet_engines.png"))
BIGGER_GUNS = pygame.image.load(os.path.join("assets", "bigger_guns.png"))
GOLDEN_SHOT = pygame.image.load(os.path.join("assets", "golden_shot.png"))
CONCENTRATED_BEAM = pygame.image.load(os.path.join("assets", "concentrated_beam.png"))
BOOSTERS = pygame.image.load(os.path.join("assets", "checkmark.png"))
FREEZE = pygame.image.load(os.path.join("assets", "checkmark.png"))
ITEMS_PNG = [LUCKY_COIN, BETTER_LASERS, JET_ENGINES, BIGGER_GUNS, GOLDEN_SHOT, CONCENTRATED_BEAM, MULTISHOT, BOOSTERS, FREEZE]

# Abilities PNG

ABILITIES_PNG = []

ITEM_TO_PNG = {
    'Lucky Coin' : LUCKY_COIN, 
    'Better Lasers': BETTER_LASERS, 
    'Jet Engines' : JET_ENGINES, 
    'Bigger Guns' : BIGGER_GUNS, 
    'Golden Shot' : GOLDEN_SHOT, 
    'Concentrated Beam' : CONCENTRATED_BEAM, 
    'Multishot' : MULTISHOT,
    'Boosters' : BOOSTERS, 
    'Freeze' : FREEZE,
}

### SFX
pygame.mixer.init()

PEW1 = pygame.mixer.Sound(os.path.join("assets", "sfx", "pew1.wav"))
CRASH = pygame.mixer.Sound(os.path.join("assets", "sfx", "crash.wav"))

LEVELS = {
    1: [["red", 5]],
    2: [["red", 6], ["", 3], ["green", 4]],
    3: [["red", 10], ["", 3], ["green", 5]],
    4: [["red", 3], ["", 2], ["green", 3], ["red", 4], ["", 2], ["green", 4], ["red", 5], ["", 2], ["green", 5]],
    5:[["blue", 4], ["", 3], ['red', 5], ["", 2], ["green", 5], ["", 3], ["blue", 4]]
}

YELLOW_MIN = {
    "color" : 'yellow',
    "vel" : 20,
    "laser_vel" : 15,
    "dmg" : 10,
    "health" : 100,
    "cooldown" : 60,
    "critchance" : 0,
    "critdmg" : 200
    }

YELLOW_MAX = {
    "color" : 'yellow',
    "vel" : 50,
    "laser_vel" : 15,
    "dmg" : 15,
    "health" : 200,
    "cooldown" : 45,
    "critchance" : 5,
    "critdmg" : 250
}

MAX_STATS = {
    "vel" : 130,
    "laser_vel" : 15,
    "dmg" : 30,
    "health" : 500,
    "cooldown" : 35,
    "critchance" : 15,
    "critdmg" : 300
}