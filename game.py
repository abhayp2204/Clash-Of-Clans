# Classes
from src.entity import *
from src.building import *

# Misc
from src.variables import *
from src.canvas import *
from src.controls import *
from src.util import *
from src.input import *
from src.stats import *

def init():
    # Color codes don't work on Windows without this command
    # Autoreset: Avoid clearing color everytime
    colorama.init(autoreset=True)

    # Setup terminal
    os.system("clear")
    os.system("stty -echo")
    hide_cursor()

    # Setup village
    set_border()
    
    K.draw(4, 10, 1, 1)
    
    # Townhall
    th.draw(int((CENTER_X - TOWNHALL_SIZE[0])/2), CENTER_Y - TOWNHALL_SIZE[1], TOWNHALL_SIZE[0], TOWNHALL_SIZE[1])  

    # Huts
    hut = [Building("Hut",
                    HUT_COLOR,
                    HUT_SIZE,
                    HUT_HEALTH)
            for _ in range(0, NUM_HUTS)]
    
    for i in range(NUM_HUTS):
        x = random.randint(1, CENTER_X - HUT_SIZE[0] - 1)
        y = random.randint(1, CANVAS_HEIGHT - HUT_SIZE[1])
        hut[i].draw(10, 10, HUT_SIZE[0], HUT_SIZE[1])
        
        
    # Cannons
    cannon = [Cannon("Cannon",
                     CANNON_COLOR,
                     CANNON_SIZE,
                     CANNON_HEALTH,
                     CANNON_DAMAGE,
                     CANNON_FIRE_RATE,
                     CANNON_SPAN)
                for _ in range(0, NUM_CANNONS)]
    
    for i in range(NUM_CANNONS):
        x = int((CENTER_X - TOWNHALL_SIZE[0])/2) + (not not i)*TOWNHALL_SIZE[0] - (not i)*CANNON_SIZE[0]
        y = CENTER_Y - TOWNHALL_SIZE[1]
        cannon[i].draw(x, y, CANNON_SIZE[0], CANNON_SIZE[1])
        
        
    # Spawn Points
    for i in range(NUM_SPAWN_POINTS):
        P = SPAWN_POINT[i]
        x = P[0]
        y = P[1]
        CANVAS[y][x] = SPAWN_POINT_COLOR + "█"
        CANVAS[y][x+1] = SPAWN_POINT_COLOR + "█"
         
START_TIME = time.time()
getch = Get()
init()

while(not game_over):
    # break

    key = input_to(getch)
    input_handler(key)
    
    for B in Barbarian:
        if(timesteps == B.move_time):
            continue
        B.move_time = timesteps
        target = Building.all[0]
        attacking = B.move(target)
        
        # Re-color
        CANVAS[B.Y][B.X] = B.color + "█"
        CANVAS[B.Y][B.X + 1] = B.color + "█"
        
        # Attempt to ttack once every three timesteps
        if(timesteps % 3 != 0):
            continue
        
        # Not near a building
        if(not attacking):
            continue
        
        # Already attacked in the given timestep
        if(timesteps == B.attack_time):
            continue
        
        B.attack_time = timesteps
        B.attack(target)
        
    # Clear destroyed buildings
    for building in Building.all:
        if(building.alive and building.health <= 0):
            building.alive = False
            building.draw(building.X, building.Y, building.size[0], building.size[1])
    
    if(game_over):
        break
    
    current_time = time.time()
    seconds = current_time - START_TIME
    timesteps = int(seconds / TIMESTEP)
    
    # Display
    os.system("clear")
    print_canvas()
    
    print(th.health)
    # print(CANVAS[K.Y][K.X + 1])
    
# Exit
print()
show_cursor()
os.system("stty echo")