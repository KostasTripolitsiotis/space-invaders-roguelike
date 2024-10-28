from const import *
from func import get_savefile, getShipStats

pcolor = "yellow"
stats = getShipStats(pcolor)
pvel = stats['vel']
plaser_vel = stats['laser_vel']
pdmg = stats['dmg']
phealth = stats['health']
pcooldown = stats['cooldown']
pcash = get_savefile()['cash']
pcritchance = stats['critchance']
pcritdmg = stats['critdmg']

player = {
    "color" : pcolor,
    "spaceship_img" : YELLOW_SPACE_SHIP, 
    "laser_img" : YELLOW_LASER, 
    "vel" : pvel,
    "laser_vel" : plaser_vel,
    "dmg" : pdmg,
    "health" : phealth,
    "cooldown" : pcooldown,
    "cash" : pcash,
    "critchance" : pcritchance,
    "critdmg" : pcritdmg
}

yellow = {
    "color" : 'yellow',
    "vel" : 20,
    "laser_vel" : 15,
    "dmg" : 10,
    "health" : 100,
    "cooldown" : 60,
    "critchance" : 0,
    "critdmg" : 200
}

blue = {
    "color" : "blue", 
    "spaceship_img" : BLUE_SPACE_SHIP, 
    "laser_img" : BLUE_LASER, 
    "vel" : 50,
    "laser_vel" : 15,
    "health" : 10,
    "cooldown" : 100000,
    "worth" : 50,
    "dmg" : 10, 
    "critchance" : 0, 
    "critdmg" : 200
}

green = {
    "color" : "green", 
    "spaceship_img" : GREEN_SPACE_SHIP, 
    "laser_img" : GREEEN_LASER, 
    "vel" : 10,
    "laser_vel" : 15,
    "health" : 20,
    "cooldown" : 200,
    "worth" : 20,
    "dmg" : 10, 
    "critchance" : 0, 
    "critdmg" : 200
}

red = {
    "color" : "red", 
    "spaceship_img" : RED_SPACE_SHIP, 
    "laser_img" : RED_LASER, 
    "vel" : 20,
    "laser_vel" : 15,
    "health" : 12,
    "cooldown" : 100,
    "worth" : 10,
    "dmg" : 10, 
    "critchance" : 0, 
    "critdmg" : 200
}