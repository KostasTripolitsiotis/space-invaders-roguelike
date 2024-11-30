import shelve
import random
import math
import pygame
from const import *

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def spawn_enemy(color, player, level):
    from player import Player
    from enemy import Enemy
    from stats import blue, green, red
    player:Player = player
    level_mod = 1+((level-1) * 0.05)
    mod = {
        "cooldown" : player.enemy_modifiers["cooldown"],
        "vel": player.enemy_modifiers["vel"]*level_mod,
        "health": player.enemy_modifiers["health"]*level_mod,
        "cooldown": player.enemy_modifiers["cooldown"]*(1/level_mod),
        "dmg": player.enemy_modifiers["dmg"]*level_mod,
        "critchance": player.enemy_modifiers["critchance"]*int(level_mod),
        "critdmg": player.enemy_modifiers["critdmg"]*level_mod
    }
    match color:
        case "red":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*mod["cooldown"], red["vel"]*level_mod, 
                          red["laser_vel"], red["health"]*mod["health"], red["cooldown"]*mod["cooldown"], red["worth"],
                          red["dmg"]*mod["dmg"], red["critchance"]*mod["critchance"], red["critdmg"]*mod["critdmg"])
        case "blue":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*mod["cooldown"], blue["vel"]*level_mod, 
                          blue["laser_vel"], blue["health"]*mod["health"], blue["cooldown"]*mod["cooldown"], blue["worth"],
                          blue["dmg"]*mod["dmg"], blue["critchance"]*mod["critchance"], blue["critdmg"]*mod["critdmg"])
        case "green":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4*mod["cooldown"], green["vel"]*level_mod, 
                          green["laser_vel"], green["health"]*mod["health"], green["cooldown"]*mod["cooldown"], green["worth"],
                          green["dmg"]*mod["dmg"], green["critchance"]*mod["critchance"], green["critdmg"]*mod["critdmg"])
    
    
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

def save_onExit(cash= None, options = None) -> None:
    from stats import player
    with shelve.open('savefile/savefile') as f:
        if cash != None:
            f['cash'] = cash
        if options != None:
            f['options'] = options
    player['cash'] = cash

def update_res(res):
    pygame.display.set_mode(res)
    f = get_savefile()
    f['options']['res'] = res
    save_onExit(options=f['options'])

def print_savefile() -> None:
    with shelve.open('savefile/savefile') as f:
        for item in f:
            print(f'{item} = {f[item]}')

def get_savefile():
    with shelve.open('savefile/savefile') as f:
        file = {}
        for item in f:
            file[item] = f[item]
        return file
 
def savefile_toString():
    f = get_savefile()
    savefile = ""
    for item in f:
        savefile += str(item)+": "+ str(f[item]) +"\n"
    return savefile
            
def getShipStats(color:str) ->dict:
    with shelve.open('savefile/savefile') as f:
        return f[color]
    
def saveStats(color, stats):
    from stats import player
    with shelve.open('savefile/savefile') as f:
        f[color] = stats
    for stat in stats:
        player[stat] = stats[stat]
        
def editItems(item:str, op='add'):
    """op = 'add' | 'rm' to add or remove from selected items\n
    'lock' | 'unlock' to modify locked/unlocked\n
    Returns from savefile"""
    with shelve.open('savefile/savefile') as f:
        temp:list = []
        if item in f['items_unlocked']: # add/rm/lock - if item exists in ulocked items
            if op == 'add' and not(item in f['items_selected']):
                temp = f['items_selected']
                temp.append(item)
                f['items_selected'] = temp
            elif op == 'rm' and item in f['items_selected']:
                temp = f['items_selected']
                temp.remove(item)
                f['items_selected'] = temp
            elif op == 'lock':
                temp = f['items_unlocked']
                temp.remove(item)
                f["items_unlocked"] = temp
                if item in f['items_selected']: # if it was seletcted -> de-select it
                    editItems(item, 'rm')
        else: # unlock
            if op == 'unlock' and not(item in f['items_unlocked']):
                temp = f["items_unlocked"]
                temp.append(item)
                f["items_unlocked"] = temp
            
def getSavedItems(op='equiped') -> list[str]:
    """op = equiped | unlocked
    Returns from savefile"""
    with shelve.open('savefile/savefile') as f:
        if op == 'equiped': return f['items_selected']
        elif op == 'unlocked': return f['items_unlocked']
        
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
    
def draw_basic_button(button:pygame.Rect, label:str, fontzise: pygame.font.SysFont = OPTIONS['fontsize'], thic = 1, border_color = (255, 255, 255), color = (29, 27, 27)):
    pygame.draw.rect(WIN, color, button)
    font = pygame.font.SysFont("lucidaconsole", fontzise)
    label = font.render(label, 1, (238, 240, 240))
    WIN.blit(label, (button.x + (button.width - label.get_width())/2, button.y + (button.height - label.get_height())/2))
    draw_border(WIN, (button.x, button.y), (button.x+button.width, button.y+button.height), thic, border_color) 
     
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
    from item import BetterLasers, LuckyCoin, JetEngine, BiggerGuns, GoldenShot, ConcentratedBeam, Multishot, Boosters, Freeze
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
        case 'Boosters' : player.active_items.append(Boosters())
        case 'Freeze' : player.active_items.append(Freeze())
        case _: pass
    for item in player.items:
        if item.type_modifier == "rep":
            item.modify(player)
        
def draw_static_bg():
    try:
        pygame.draw.rect(WIN, C_BACKROUND, (0, 0, SWIDTH, HEIGHT))
    except pygame.error as error:
        print(error)

def upgrade(spaceship:str, stat:str) -> int | float:
    spaceship_stats = {}
    stats_max = {}
    stats_min = {}
    step = 5 # Step is how many upgrades before it reach its maximum
    match spaceship:
        case "yellow": 
            spaceship_stats = getShipStats('yellow')
            stats_max = YELLOW_MAX
            stats_min = YELLOW_MIN
        case _:pass
        
    if spaceship_stats[stat] >= stats_max[stat] and stat != "cooldown": # if stat is max do nothing
        return None
    elif spaceship_stats[stat] <= stats_max[stat] and stat == "cooldown": # if stat is max do nothing
        return None
    else: # if player doenst have enough cash do nothing, else reduce cash
        player_cash = get_savefile()['cash']
        cost = get_upgrade_cost(stat)
        if player_cash - cost < 0: return None
        else: save_onExit(cash=player_cash-cost)
    
    if stat != "cooldown":
        spaceship_stats[stat] += (stats_max[stat]-stats_min[stat])/step # Increase by an amount so this*step = max
        if spaceship_stats[stat] > stats_max[stat]: spaceship_stats[stat] = stats_max[stat]
    else:
        spaceship_stats[stat] -= (stats_min[stat]-stats_max[stat])/step # Increase by an amount so this*step = max
        if spaceship_stats[stat] < stats_max[stat]: spaceship_stats[stat] = stats_max[stat]   
    
    saveStats(spaceship, spaceship_stats)
    return spaceship_stats[stat]
    
def resetYellow() -> dict:  
    player = {
    "color" : 'yellow',
    "vel" : 20,
    "laser_vel" : 15,
    "dmg" : 10,
    "health" : 100,
    "cooldown" : 60,
    "critchance" : 0,
    "critdmg" : 200
    }
    saveStats('yellow', player)
    return player

def get_item_cost(item_name:str) -> int:
    cost = 0
    match item_name:
        case 'Better Lasers': cost = 200
        case 'Jet Engines': cost = 200
        case 'Bigger Guns': cost = 200
        case 'Lucky Coin': cost = 200
        case 'Golden Shot': cost = 200
        case 'Concentrated Beam': cost = 200
        case 'Multishot' : cost = 200
        case 'Boosters' : cost = 200
        case 'Freeze' : cost = 200
        case _: print("No such item")
    return cost

def get_upgrade_cost(stat_name:str) -> int:
    cost = 500
    stat = get_savefile()["yellow"][stat_name]
    stat_max = YELLOW_MAX[stat_name]
    stat_min = YELLOW_MIN[stat_name]
    
    if stat == stat_max: 
        return 0
    
    if stat_name != "cooldown":
        step = (stat_max-stat_min)/5
        while ((stat+step) != stat_max):
            stat += step
            cost -= 100
        
    else: 
        step = (stat_min-stat_max)/5
        while ((stat-step) != stat_max):
            stat -= step
            cost -= 100
    
    return cost

def unlockItem(item_name):
    player_cash = get_savefile()['cash']
    item_cost = get_item_cost(item_name)
    
    if(item_cost > player_cash):
        return False
    else:
        save_onExit(player_cash-item_cost)
        editItems(item_name, "unlock")
        return True
