from const import *
import random

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def spawn_enemies(level):
    from enemy import Enemy
    enemies = []
    wave_length = level * 5
    for i in range(wave_length):
        choice = random.choice(["red", "blue", "green"])
        enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), choice, 4)
        enemies.append(enemy)
    
    return enemies