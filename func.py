import shelve
import random
from const import *

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def spawn_enemies(level: int):
    from enemy import Enemy
    from stats import blue, green, red
    enemies = []
    wave_length = level * 5
    for i in range(wave_length):
        choice = random.choice(["red", "blue", "green"])
        match choice:
            case "red":
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), choice, 4, red["vel"], red["laser_vel"], red["health"], red["cooldown"], red["worth"])
            case "blue":
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), choice, 4, blue["vel"], blue["laser_vel"], blue["health"], blue["cooldown"], blue["worth"])
            case "green":
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), choice, 4, green["vel"], green["laser_vel"], green["health"], green["cooldown"], green["worth"])
        enemies.append(enemy)
    
    return enemies

def save(cash: int) -> None:
    with shelve.open('savefile/savefile') as f:
        f['cash'] = cash
def open_savefile() -> list:
    with shelve.open('savefile/savefile') as f:
        cash = f['cash']
    return cash

def draw_border(surface: pygame.Surface, x: int, y: int):
    for i in range(4):
        pygame.draw.rect(surface, (100,100,100), (x-i,y-i,99,99), 1)
        
def levelup(stat: str, player):
    match stat:
        case '+5 Speed': player.vel += 5
        case '-10% Cooldown': player.cooldown  = int(player.cooldown * 0.9)
        case '+5 Damage': player.dmg += 5
        case '+10 Health': 
            player.max_health += 10
            player.health += 10
        case _: pass
        