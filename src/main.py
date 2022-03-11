from .variables import *
from .building import *
from .entity import *
from .setup import *

def get_target(B):
    min = 1000
    target = th
    for b in Building.all:
        d = distance(B, b)
        if(d < min):
            min = d
            target = b
    return target

def handle_barbarians(timesteps):
    for B in Entity.Barbarians:
        
        # Ignore dead barbarians
        if not B.alive:
            continue
        
        target = get_target(B)
        if(B.target_wall != th and B.target_wall.alive):
            target = B.target_wall
            
        attacking = B.within_attack_range(target)
        
        if(timesteps == B.move_time):
            continue
        
        B.move_time = timesteps
        B.move(target)
        
        # Re-color
        CANVAS[B.Y][B.X] = B.color + "█"
        CANVAS[B.Y][B.X + 1] = B.color + "█"
        
        # Attempt to attack once every three timesteps
        if(timesteps % 3 == 0 and attacking and timesteps != B.attack_time):
            B.attack_time = timesteps
            B.attack(target)
            
def handle_cannons(timesteps):
    for C in Cannon.all:
        if not C.alive:
            continue
        
        # Attempt to attack once every two timesteps
        if(timesteps % 2 == 0 and timesteps != C.fire_time):
            C.fire_time = timesteps
            
            for B in Entity.Barbarians:
                C.in_range(B)
            C.in_range(K)
            
            if not C.targets:
                continue

            while(C.targets and not C.targets[0].alive):
                C.targets.pop(0)
                
            if C.targets:
                C.fire(C.targets[0])
                
def grim_reaper():
    # Buildings
    i = 0
    for building in Building.all:
        if(building.alive and building.health <= 0):
            building.alive = False
            Building.all.pop(i)
            building.draw(building.X, building.Y)
        i += 1
        
    # Barbarians
    for B in Entity.Barbarians:
        if(B.alive and B.health <= 0):
            B.alive = False
            CANVAS[B.Y][B.X] = " "
            CANVAS[B.Y][B.X + 1] = " "
        
    # King
    if(K.alive and K.health <= 0):
        K.alive = False
        CANVAS[K.Y][K.X] = " "
        CANVAS[K.Y][K.X + 1] = " "
        
    # Walls
    i = 0
    for w in Building.walls:
        if(w.alive and w.health <= 0):
            w.alive = False
            Building.walls.pop(i)
            w.draw(w.X, w.Y)
        i += 1