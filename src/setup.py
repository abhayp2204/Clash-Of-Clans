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
    walls = []
    for i in range(50):
        walls.append(Building("Wall", WALL_COLOR, WALL_SIZE, WALL_HEALTH))

    walls[0].draw(7, 11)
    walls[1].draw(7, 5)
    walls[2].draw(8, 5)
    walls[3].draw(9, 5)
    walls[4].draw(10, 5)
    walls[5].draw(7, 6)
    walls[6].draw(7, 7)
    walls[7].draw(7, 8)
    walls[8].draw(7, 9)
    walls[9].draw(7, 10)
    
    walls[10].draw(22, 11)
    walls[11].draw(22, 12)
    walls[12].draw(22, 13)
    walls[13].draw(22, 14)
    walls[14].draw(22, 15)
    walls[15].draw(22, 16)
    walls[16].draw(22, 17)
    walls[17].draw(22, 33)
    
    walls[18].draw(23, 11)
    walls[19].draw(24, 11)
    walls[20].draw(25, 11)
    walls[21].draw(26, 11)
    walls[22].draw(27, 11)
    walls[23].draw(28, 11)
    walls[24].draw(29, 11)
    walls[25].draw(30, 11)
    walls[26].draw(31, 11)
    walls[27].draw(32, 11)
    walls[28].draw(33, 11)
    
    walls[29].draw(33, 12)
    walls[30].draw(33, 13)
    walls[31].draw(33, 14)
    walls[32].draw(33, 15)
    walls[33].draw(33, 16)
    walls[34].draw(33, 17)
    walls[35].draw(33, 18)
    
    walls[36].draw(22, 18)
    walls[37].draw(23, 18)
    walls[38].draw(24, 18)
    walls[39].draw(25, 18)
    walls[40].draw(26, 18)
    walls[41].draw(27, 18)
    walls[42].draw(28, 18)
    walls[43].draw(29, 18)
    walls[44].draw(30, 18)
    walls[45].draw(31, 18)
    walls[46].draw(32, 18)
    walls[47].draw(33, 18)
    return

         
def end_game():
    show_cursor()
    os.system("stty echo")
    exit()