from .variables import *
from .display import *

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
    
    K.draw(4, 10)
    
    # Townhall
    th.draw(int((CENTER_X - TOWNHALL_SIZE[0])/2), CENTER_Y - TOWNHALL_SIZE[1])  

    # Huts
    hut = [Building("Hut",
                    HUT_COLOR,
                    HUT_SIZE,
                    HUT_HEALTH)
            for _ in range(0, NUM_HUTS)]
    
    for i in range(NUM_HUTS):
        x = random.randint(1, CENTER_X - HUT_SIZE[0] - 1)
        y = random.randint(1, CANVAS_HEIGHT - HUT_SIZE[1])
        hut[i].draw(10, 10)
          
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
        left_offset = 23
        gap = 8
        x = left_offset + i*gap
        y = CENTER_Y - TOWNHALL_SIZE[1]
        cannon[i].draw(x, y)
        
    # Spawn Points
    for i in range(NUM_SPAWN_POINTS):
        P = SPAWN_POINT[i]
        x = P[0]
        y = P[1]
        CANVAS[y][x] = SPAWN_POINT_COLOR + "█"
        CANVAS[y][x+1] = SPAWN_POINT_COLOR + "█"
        
    # Wall
    W1 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W2 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W3 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W4 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W5 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W6 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W7 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W8 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W9 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)
    W10 = Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH)

    W1.draw(7, 5)
    W2.draw(8, 5)
    W3.draw(9, 5)
    W4.draw(10, 5)
    W5.draw(7, 6)
    W6.draw(7, 7)
    W7.draw(7, 8)
    W8.draw(7, 9)
    W9.draw(7, 10)
    W10.draw(7, 11)
         
def end_game():
    show_cursor()
    os.system("stty echo")
    exit()