import shelve
import random
from const import *

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def spawn_enemy(color, items):
    from enemy import Enemy
    from stats import blue, green, red
    match color:
        case "red":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4, red["vel"], red["laser_vel"], red["health"], red["cooldown"], red["worth"])
        case "blue":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4, blue["vel"], blue["laser_vel"], blue["health"], blue["cooldown"], blue["worth"])
        case "green":
            enemy = Enemy(random.randrange(50+OFFSET, WIDTH-100), random.randrange(-100, -50), color, 4, green["vel"], green["laser_vel"], green["health"], green["cooldown"], green["worth"])
    
    
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
    with shelve.open('spacerogue/savefile/savefile') as f:
        f['cash'] = cash
def open_savefile() -> list:
    with shelve.open('spacerogue/savefile/savefile') as f:
        cash = f['cash']
    return cash

def draw_border(surface: pygame.Surface, x: int, y: int):
    for i in range(4):
        pygame.draw.rect(surface, (100,100,100), (x-i,y-i,99,99), 1)
        
def levelup(choice: str, player):
    from item import BetterLasers, LuckyCoin
    from player import Player
    player:Player = player
    match choice: #for stat changes
        case '+5 Speed': player.vel += 5
        case '-10% Cooldown': 
            player.cooldown  = int(player.cooldown * 0.9)
            if player.cooldown < 3:
                player.cooldown = 3
        case '+5 Damage': player.dmg += 5
        case '+10 Health': 
            player.max_health += 10
            player.health += 10
        case '+1 Life': player.lives += 1
        case '+5% Crit': player.critchance += 5
        case '+20% Crit Dmg': player.critdmg += 20
        case _: pass
        
    match choice: #for items
        case 'Better Lasers': player.items.append(BetterLasers())
        
    for item in player.items:
        if item.type_modifier == "add":
            item.modify_player(player)
    for item in player.items:
        if item.type_modifier == "mult":
            item.modify_player(player)
        
def draw_static_bg():
    pygame.draw.rect(WIN, (55, 53, 59), (0, 0, SWIDTH, HEIGHT))
