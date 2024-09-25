import pygame
import os
from win32api import GetSystemMetrics

# SWIDTH = GetSystemMetrics(0)
# OFFSET = int(SWIDTH/6)
# WIDTH, HEIGHT = int(2*SWIDTH/3), GetSystemMetrics(1)
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
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

COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

LEVELUP_CHOICES = ['+5 Speed', '-10% Cooldown', '+5 Damage', '+10 Health']

LEVELS = {
    1: [["red", 5]],
    2: [["red", 6], ["green", 4]],
    3: [["red", 10], ["green", 5]]
}