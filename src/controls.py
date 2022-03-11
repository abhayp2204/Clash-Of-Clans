from .variables import *
from .entity import *
from .spell import *
from .util import *
from .setup import *

def input_handler(key, timesteps):
    # Game controls
    if(key == "q"):
        end_game(0)
        
    # Disable king controls when dead
    if not K.alive:
        return
    
    # King movement
    if(key == "w"):
        K.move_up()
    if(key == "a"):
        K.move_left()
    if(key == "s"):
        K.move_down()
    if(key == "d"):
        K.move_right()
        
    # Attack
    if(key == " "):
        K.attack()
        
    # Spells
    if(key == "r"):
        if(Rage.number > 0 and not Rage.active):
            Rage.apply(timesteps)
            Rage.number -= 1
    if(key == "h"):
        if(Heal.number > 0):
            Heal.apply(timesteps)
            Heal.number -= 1
        
    if(key == "1"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS):
            return
        
        B = Entity("Barbarian", BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED)
        
        B.X = SPAWN_POINT_A[0]
        B.Y = SPAWN_POINT_A[1] + 1
    if(key == "2"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS):
            return
        
        B = Entity("Barbarian", BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED)
        
        B.X = SPAWN_POINT_B[0] - 4
        B.Y = SPAWN_POINT_B[1]
    if(key == "3"):
        if(len(Entity.Barbarians) == MAX_BARBARIANS):
            return
        
        B = Entity("Barbarian", BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED)
        
        B.X = SPAWN_POINT_C[0] + 2
        B.Y = SPAWN_POINT_C[1]