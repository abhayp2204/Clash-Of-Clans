from .variables import *
from .building import *
from .entity import *
from .setup import *


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
        if(timesteps % int(6/B.speed) != 0):
            continue
        
        B.move_time = timesteps
        B.move(target)
        
        # Attempt to attack once every three timesteps
        if(attacking and timesteps != B.attack_time):
            B.attack_time = timesteps
            B.attack(target)
            
def handle_archers(timesteps):
    for A in Entity.Archers:
        # Ignore dead archers
        if not A.alive:
            continue
        
        target = get_target(A)
        if(A.target_wall != th and A.target_wall.alive):
            target = A.target_wall
            
        attacking = A.within_attack_range(target)
        
        if(timesteps == A.move_time):
            continue
        if(timesteps % int(6/A.speed) != 0):
            continue
        
        A.move_time = timesteps
        
        if not attacking:
            A.move(target)
        
        # Attempt to attack once every three timesteps
        if(attacking and timesteps != A.attack_time):
            A.attack_time = timesteps
            A.attack(target)
            
def handle_balloons(timesteps):
    for Bl in Entity.Balloons:
        # Ignore dead balloons
        if not Bl.alive:
            continue
        
        Bl.damage = BALLOON_DAMAGE
        
        target = get_target(Bl)
        attacking = Bl.within_attack_range(target)
        
        if(timesteps == Bl.move_time):
            continue
        if(timesteps % int(6/Bl.speed) != 0):
            continue
        
        Bl.move_time = timesteps
        
        if not attacking:
            Bl.move(target)
        
        # Attempt to attack once every three timesteps
        if(attacking and timesteps != Bl.attack_time):
            Bl.attack_time = timesteps
            Bl.attack(target)
    
def handle_eagle_arrow(H):
    # H.active means the arrows are still in the air
    if H.name == "Archer Queen" and H.active:
        # Wait for the arrows to land (1 second later)
        if time.time() - H.time >= QUEEN_POWER_ATTACK_TIME:
            H.use_eagle_arrow()
            H.active = False
    th.message = H.num_power_attack
    
def handle_witch(H, F, L, timesteps):
    if not H.alive:
        end_game(0, F, L)
    
    W.damage = WITCH_DAMAGE
    if not W.alive:
        return
    if(timesteps % 3 == 0):
        W.move(K)
        if(W.within_attack_range(K)):
            W.attack(K)
            
def handle_cannons(H, timesteps):
    for C in Defender.cannons:
        if not C.alive:
            continue
        
        # Attempt to attack once every two timesteps
        if(timesteps % 2 == 0 and timesteps != C.fire_time):
            C.fire_time = timesteps
            
            for B in Entity.Barbarians:
                C.in_range(B)
            for A in Entity.Archers:
                C.in_range(A)
            for Bl in Entity.Balloons:
                C.in_range(Bl)
            
            
            C.in_range(H)
            
            if not C.targets:
                continue

            while(C.targets and not C.targets[0].alive):
                C.targets.pop(0)
                
            if C.targets:
                C.fire(C.targets[0])
                
def handle_wizard_towers(H, timesteps):
    for Wt in Defender.wizard_towers:
        if not Wt.alive:
            continue
        
        # Attempt to attack once every two timesteps
        if(timesteps % 2 == 0 and timesteps != Wt.fire_time):
            Wt.fire_time = timesteps
            
            for B in Entity.Barbarians:
                Wt.in_range(B)
            for A in Entity.Archers:
                Wt.in_range(A)
            for Bl in Entity.Balloons:
                Wt.in_range(Bl)
            Wt.in_range(H)
            
            if not Wt.targets:
                continue

            while(Wt.targets and not Wt.targets[0].alive):
                Wt.targets.pop(0)
                
            if Wt.targets:
                Wt.fire(Wt.targets[0])
   
def handle_buildings(timesteps):
    for b in Building.all:
        perc = 100*(b.health/b.max_health)
        b.draw(b.X, b.Y)
    for w in Building.walls:
        if w.alive:
           w.draw(w.X, w.Y) 
                
def grim_reaper():
    # Buildings
    i = 0
    for b in Building.all:
        if(b.alive and b.health <= 0):            
            b.alive = False
            Building.all.pop(i)
            
            # if(not th.alive and not W.alive and not W.killed):
            #     trap()
                
            b.draw(b.X, b.Y)
        i += 1
        
    i = 0
    for D in Defender.all:
        if D.health <= 0:
            D.alive = False
            Defender.all.pop(i)
        i += 1
        
    i = 0
    for C in Defender.cannons:
        if C.health <= 0:
            C.alive = False
            Defender.cannons.pop(i)
        i += 1
        
    i = 0
    for W in Defender.wizard_towers:
        if W.health <= 0:
            W.alive = False
            Defender.wizard_towers.pop(i)
        i += 1
        
    # Barbarians
    i = 0
    for B in Entity.all:
        if(B.alive and B.health <= 0):
            B.alive = False
            Entity.all.pop(i)
            
            CANVAS[B.Y][B.X] = " "
            CANVAS[B.Y][B.X + 1] = " "
        i += 1
    
    # Walls
    i = 0
    for w in Building.walls:
        if(w.alive and w.health <= 0):
            w.alive = False
            Building.walls.pop(i)
            w.draw(w.X, w.Y)
        i += 1
   
def handle_aerial():
    if th.alive:
        th.draw(th.X, th.Y)
    
    for Bl in Entity.Balloons:
        if Bl.alive:
            for i in range(X_SCALE):
                CANVAS[Bl.Y][Bl.X + i] = Back.BLACK + Fore.WHITE + Bl.letters[i] + Fore.RESET + Back.RESET
                
def get_target(E):
    min = 1000
    target = th
    for b in Building.all:
        if not b.alive:
            continue
        
        # Balloons prioritorize defensive buildings
        defensive_buildings_present = False

        if E.name == "Balloon":
            for D in Defender.all:
                if D.alive:
                    defensive_buildings_present = True
                    break
            
        if defensive_buildings_present and b not in Defender.all:
            continue
        
        d = distance(E, b)
        if(d < min):
            min = d
            target = b
        
    return target
        
def trap():
    return
    W.alive = True
    for B in Entity.Barbarians:
        B.alive = False
        B.erase()
    
    for y in [6, 24]:
        for x in range(20, 60):
            CANVAS[y][x] = Fore.RED + "*"
    for x in [20, 60]:
        for y in range(6, 25):
            CANVAS[y][x] = Fore.RED + "*"
    W.draw(38, 22)