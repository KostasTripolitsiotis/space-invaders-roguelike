from const import *
from func import open_savefile
import shelve

pcolor = "yellow"
pvel = 20
plaser_vel = 15
pdmg = 10
phealth = 100
pcooldown = 60
pcash = open_savefile()
pcritchance = 50

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
    "critchance" : pcritchance
}

yellow = {
    "color" : 'yellow',
    "spaceship_img" : YELLOW_SPACE_SHIP, 
    "laser_img" : YELLOW_LASER, 
    "vel" : 20,
    "laser_vel" : 15,
    "health" : 100,
    "cooldown" : 60,
}

blue = {
    "color" : "blue", 
    "spaceship_img" : BLUE_SPACE_SHIP, 
    "laser_img" : BLUE_LASER, 
    "vel" : 50,
    "laser_vel" : 15,
    "health" : 10,
    "cooldown" : 100000,
    "worth" : 50
}

green = {
    "color" : "green", 
    "spaceship_img" : GREEN_SPACE_SHIP, 
    "laser_img" : GREEEN_LASER, 
    "vel" : 10,
    "laser_vel" : 15,
    "health" : 20,
    "cooldown" : 200,
    "worth" : 20
}

red = {
    "color" : "red", 
    "spaceship_img" : RED_SPACE_SHIP, 
    "laser_img" : RED_LASER, 
    "vel" : 20,
    "laser_vel" : 15,
    "health" : 12,
    "cooldown" : 100,
    "worth" : 10
}