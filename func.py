import shelve
import random
import math
import pygame
from const import *

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def spawn_enemy(color, player):
    from player import Player
    from enemy import Enemy
    from stats import blue, green, red
    player:Player = player
    match color:
        case "red":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*player.enemy_modifiers["cooldown"], red["vel"]+player.enemy_modifiers["vel"], 
                          red["laser_vel"], red["health"]+player.enemy_modifiers["health"], red["cooldown"]*player.enemy_modifiers["cooldown"], red["worth"],
                          red["dmg"]+player.enemy_modifiers["dmg"], red["critchance"]+player.enemy_modifiers["critchance"], red["critdmg"]+player.enemy_modifiers["critdmg"])
        case "blue":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*player.enemy_modifiers["cooldown"], blue["vel"]+player.enemy_modifiers["vel"], 
                          blue["laser_vel"], blue["health"]+player.enemy_modifiers["health"], blue["cooldown"]*player.enemy_modifiers["cooldown"], blue["worth"],
                          blue["dmg"]+player.enemy_modifiers["dmg"], blue["critchance"]+player.enemy_modifiers["critchance"], blue["critdmg"]*player.enemy_modifiers["critdmg"])
        case "green":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*player.enemy_modifiers["cooldown"], green["vel"]+player.enemy_modifiers["vel"], 
                          green["laser_vel"], green["health"]+player.enemy_modifiers["health"], green["cooldown"]*player.enemy_modifiers["cooldown"], green["worth"],
                          green["dmg"]+player.enemy_modifiers["dmg"], green["critchance"]+player.enemy_modifiers["critchance"], green["critdmg"]+player.enemy_modifiers["critdmg"])
    
    
    return enemy

def getEnemyWave(level:int):
    enemytype = []
    dtime = []
    if level in LEVELS:
        elist = LEVELS[level]
        for e in elist:
            for i in range(e[1]):
                enemytype.append(e[0])
                dtime.append(random.randrange(60, 120))
    else:
        for i in range(level*3):
            enemytype.append(random.choice(["red", "blue", "green"]))
            dtime.append(random.randrange(60, 120))
                
    return enemytype, dtime

def save(cash: int) -> None:
    with shelve.open('savefile/savefile') as f:
        f['cash'] = cash
def open_savefile() -> list:
    with shelve.open('savefile/savefile') as f:
        cash = f['cash']
    return cash
def getActiceSpaceship(color:str) ->dict:
    with shelve.open('savefile/test') as f:
        return f[color]
        
def draw_border(surface: pygame.Surface, point1:tuple[int, int], point2:tuple[int, int], thicness:int, color:tuple[int, int, int]):
    """point1: x, y of top left corner
       point2: x, y of bottom right corner"""
    rect1 = pygame.Rect(point1[0], point1[1], (point2[0]-point1[0]), thicness)
    rect2 = pygame.Rect(point2[0]-thicness, point1[1], thicness, point2[1]-point1[1])
    rect3 = pygame.Rect(point1[0], point2[1]-thicness, (point2[0]-point1[0]), thicness)
    rect4 = pygame.Rect(point1[0], point1[1], thicness,(point2[1]-point1[1]))
    pygame.draw.rect(surface, color, rect1)
    pygame.draw.rect(surface, color, rect2)
    pygame.draw.rect(surface, color, rect3)
    pygame.draw.rect(surface, color, rect4)
    
def draw_basic_button(button:pygame.Rect, label:str):
    pygame.draw.rect(WIN, (29, 27, 27), button)
    font = pygame.font.SysFont("lucidaconsole", OPTIONS['fontsize'])
    label = font.render(label, 1, (238, 240, 240))
    WIN.blit(label, (button.x + (button.width - label.get_width())/2, button.y + (button.height - label.get_height())/2))
    draw_border(WIN, (button.x, button.y), (button.x+button.width, button.y+button.height), 1, (255, 255, 255)) 
     
def getLevelupModifiers(player):
    from item import Item
    from player import Player
    modifier = 1
    luckycoin = False
    player:Player = player
    for item in player.items:
        if item.name == "Lucky Coin":
            modifier *= 2
            if not(item.modify()):
                luckycoin = True
            
    return modifier, luckycoin
        
def levelup(choice: str, player):
    from item import BetterLasers, LuckyCoin, JetEngine, BiggerGuns, GoldenShot, ConcentratedBeam, Multishot
    from player import Player
    player:Player = player
    modifier, unluckycoin = getLevelupModifiers(player)
    modify = 0
    match choice: #for stat changes
        case '+5 Speed': 
            modify = 5 * modifier
            if unluckycoin == False:
                player.vel += modify
            else: 
                player.enemy_modifiers["vel"] += modify
        case '-10% Cooldown': 
            modify = math.pow(0.9, modifier)
            if unluckycoin == False:
                player.cooldown  = int(player.cooldown * modify)
                if player.cooldown < 3:
                    player.cooldown = 3
            else:
                player.enemy_modifiers["cooldown"] *= modify
        case '+3 Damage': 
            modify = 3 * modifier
            if unluckycoin == False:
                player.dmg += modify
            else: 
                player.enemy_modifiers["dmg"] += modify
        case '+10 Health': 
            modify = 10 * modifier
            if unluckycoin == False:
                player.max_health += modify
                player.health += modify
            else: 
                player.enemy_modifiers["health"] += modify
        case '+1 Life': player.lives += 1
        case '+5% Crit': 
            modify = 5 * modifier
            if unluckycoin == False:
                player.critchance += modify
            else: 
                player.enemy_modifiers["critchance"] += modify
        case '+20% Crit Dmg': 
            modify = 20 * modifier
            if unluckycoin == False:
                player.critdmg += modify
            else: 
                player.enemy_modifiers["critdmg"] += modify
        case _: pass
        
    match choice: #for items
        case 'Better Lasers': player.items.append(BetterLasers())
        case 'Jet Engines': player.items.append(JetEngine())
        case 'Bigger Guns': player.items.append(BiggerGuns())
        case 'Lucky Coin': player.items.append(LuckyCoin())
        case 'Golden Shot': player.items.append(GoldenShot())
        case 'Concentrated Beam': player.items.append(ConcentratedBeam())
        case 'Multishot' : player.items.append(Multishot())
        case _: pass
    for item in player.items:
        if item.type_modifier == "rep":
            item.modify(player)
        
def draw_static_bg():
    try:
        pygame.draw.rect(WIN, (55, 53, 59), (0, 0, SWIDTH, HEIGHT))
    except pygame.error as error:
        print(error)
