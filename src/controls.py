from .building import Building
from .variables import *
from .entity import *
from .spell import *
from .util import *
from .setup import *

def input_handler(key, H, level, F, L, timesteps):
    if key is None:
        return
    key = key.lower()
    
    # Game controls
    if key == "q":
        end_game(0, F, L)
        
    # Disable king controls when dead
    if not H.alive:
        return
    
    # King movement
    if(key == "w"):
        H.move_up()
    if(key == "a"):
        H.move_left()
    if(key == "s"):
        H.move_down()
    if(key == "d"):
        H.move_right()
        
    # Attack
    if(key == " "):
        if H.name == "Barbarian King":
            H.attack()
        if H.name == "Archer Queen":
            H.attack(H.arrow_distance, H.aoe)
    if(key == "e"):
        if H.name == "Barbarian King":
            H.use_leviathan_axe()
        if H.name == "Archer Queen":
            if not H.active:
                H.active = True
                H.time = time.time()
        
    # Spells
    if(key == "r"):
        if(Rage.number > 0 and not Rage.active):
            Rage.apply(timesteps)
            Rage.number -= 1
    if(key == "h"):
        if(Heal.number > 0):
            Heal.apply(timesteps)
            Heal.number -= 1
        
    # Controls to spawn Barbarians
    if(key == "1"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS[level - 1]):
            return
        
        B = Entity("Barbarian", BARBARIAN_LETTERS, BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED, True, False)
        
        B.X = SPAWN_POINT_A[0]
        B.Y = SPAWN_POINT_A[1] + 1
        
    if(key == "2"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS[level - 1]):
            return
        
        B = Entity("Barbarian", BARBARIAN_LETTERS, BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED, True, False)
        
        B.X = SPAWN_POINT_B[0] - 4
        B.Y = SPAWN_POINT_B[1]
        
    if(key == "3"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS[level - 1]):
            return
        
        B = Entity("Barbarian", BARBARIAN_LETTERS, BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED, True, False)
        
        B.X = SPAWN_POINT_C[0] + 2
        B.Y = SPAWN_POINT_C[1]
        
        

    # Controls to spawn Archers
    if(key == "4"):
        if(len(Entity.Archers) == MAX_ARCHERS[level - 1]):
            return
        
        A = Entity("Archer", ARCHER_LETTERS, ARCHER_COLOR, ARCHER_SIZE, ARCHER_HEALTH, ARCHER_DAMAGE, ARCHER_SPEED, True, False)
        
        A.X = SPAWN_POINT_A[0]
        A.Y = SPAWN_POINT_A[1] + 1
        
    if(key == "5"):
        if(len(Entity.Archers) == MAX_ARCHERS[level - 1]):
            return
        
        A = Entity("Archer", ARCHER_LETTERS, ARCHER_COLOR, ARCHER_SIZE, ARCHER_HEALTH, ARCHER_DAMAGE, ARCHER_SPEED, True, False)
        
        A.X = SPAWN_POINT_B[0]
        A.Y = SPAWN_POINT_B[1] + 1
    if(key == "6"):
        
        if(len(Entity.Archers) == MAX_ARCHERS[level - 1]):
            return
        
        A = Entity("Archer", ARCHER_LETTERS, ARCHER_COLOR, ARCHER_SIZE, ARCHER_HEALTH, ARCHER_DAMAGE, ARCHER_SPEED, True, False)
        
        A.X = SPAWN_POINT_C[0] + 2
        A.Y = SPAWN_POINT_C[1]
        
        
        
    # Controls to spawn Balloons
    if(key == "7"):
        if(len(Entity.Balloons) == MAX_BALLOONS[level - 1]):
            return
        
        A = Entity("Balloon", BALLOON_LETTERS, BALLOON_COLOR, BALLOON_SIZE, BALLOON_HEALTH, BALLOON_DAMAGE, BALLOON_SPEED, BALLOON_LAND, BALLOON_AIR)
        
        A.X = SPAWN_POINT_A[0]
        A.Y = SPAWN_POINT_A[1] + 1
        
    if(key == "8"):
        if(len(Entity.Balloons) == MAX_BALLOONS[level - 1]):
            return
        
        A = Entity("Balloon", BALLOON_LETTERS, BALLOON_COLOR, BALLOON_SIZE, BALLOON_HEALTH, BALLOON_DAMAGE, BALLOON_SPEED, BALLOON_LAND, BALLOON_AIR)
        
        A.X = SPAWN_POINT_B[0]
        A.Y = SPAWN_POINT_B[1] + 1
        
    if(key == "9"):
        if(len(Entity.Balloons) == MAX_BALLOONS[level - 1]):
            return
        
        A = Entity("Balloon", BALLOON_LETTERS, BALLOON_COLOR, BALLOON_SIZE, BALLOON_HEALTH, BALLOON_DAMAGE, BALLOON_SPEED, BALLOON_LAND, BALLOON_AIR)
        
        A.X = SPAWN_POINT_C[0] + 2
        A.Y = SPAWN_POINT_C[1]
        
    # Admin controlls
    if key == "t":
        th.alive = False
        th.health = 0
    if key == "p":
        for B in Building.all:
            B.health = 0
            B.alive = False
        next_level(H, F, L)
    if key == "u":
        for Ht in Building.huts:
            Ht.health = 0
            Ht.alive = False