from .display import *
from .variables import *
from .input import *
from .util import *

def init():
    # Color codes don't work on Windows without this command
    # Autoreset: Avoid clearing color everytime
    colorama.init(autoreset=True)

    # Setup terminal
    os.system("clear")
    os.system("stty -echo")
    hide_cursor()
    
    # Reset Canvas
    for y in range(CANVAS_HEIGHT):
        for x in range(CANVAS_WIDTH):
            CANVAS[y][x] = " "

    # Setup village
    set_border()
    
    # Townhall
    th.draw(int((CENTER_X - TOWNHALL_SIZE[0])/X_SCALE), CENTER_Y - int(TOWNHALL_SIZE[1]/2))  

    # Huts
    for i in range(0, NUM_HUTS):
        H = Building("Hut", HUT_LETTERS, HUT_COLOR, HUT_SIZE, HUT_HEALTH)
        H.draw(HUT_POSITIONS[i][0], HUT_POSITIONS[i][1])
        
    # Cannons
    cannon = [Defender("Cannon",
                     CANNON_LETTERS,
                     CANNON_COLOR,
                     CANNON_SIZE,
                     CANNON_HEALTH,
                     CANNON_DAMAGE,
                     CANNON_FIRE_RATE,
                     CANNON_AOE,
                     CANNON_SPAN,
                     True,
                     False)
                for _ in range(0, CANNON_NUM)]
    
    cannon[0].draw(th.X - CANNON_SIZE[0] - 1, th.Y)
    cannon[1].draw(th.X + th.size[0] + 1, th.Y + th.size[1] - cannon[1].size[1])
    
    # Wizard Towers
    wt = [Defender("Wizard Tower",
                     WIZARD_LETTERS,
                     WIZARD_COLOR,
                     WIZARD_SIZE,
                     WIZARD_HEALTH,
                     WIZARD_DAMAGE,
                     WIZARD_FIRE_RATE,
                     WIZARD_AOE,
                     WIZARD_SPAN,
                     True,
                     False)
                for _ in range(0, WIZARD_NUM)]
    
    wt[0].draw(th.X, th.Y + th.size[1] + 1)
    wt[1].draw(th.X + th.size[0] - wt[1].size[0], th.Y - wt[1].size[1] - 1)
        
    # Spawn Points
    for i in range(NUM_SPAWN_POINTS):
        P = SPAWN_POINT[i]
        x = P[0]
        y = P[1]
        
        for i in range(X_SCALE):
            CANVAS[y][x+i] = SPAWN_POINT_COLOR + Fore.WHITE + SPAWN_POINT_LETTERS[i] + Back.RESET
        
    # Gold Storage
    gold_storage = [Building("Gold Storage",
                              GOLD_LETTERS,
                              GOLD_COLOR,
                              GOLD_SIZE,
                              GOLD_HEALTH)
                        for _ in range(0, GOLD_NUM)]
                        
    gold_storage[0].draw(18, 10)
    gold_storage[1].draw(20, 17)
    gold_storage[2].draw(15, 15)
    gold_storage[3].draw(23, 12)
        
    setup_walls(wt)
    
    right = select_hero()
    H = Q if right else K
    H.draw(4, 10)
    H.health = H.max_health
    
    return H

def select_hero():
    stars = 20
    lines = 2
    gap = 8
    getch = Get()
    right = False
    
    while(True):
        os.system("clear")
        print(Fore.YELLOW + "*"*stars + " CLASH OF CLANS " + "*"*stars)
        for _ in range(lines):
            print()
        print(Fore.CYAN + "Who would you like to play as? (Space to toggle, C to choose)")
        print()
        print(Fore.RED + "Barbarian King" + " "*gap + Fore.MAGENTA + "Archer Queen")
        if right:
            print(" "*(len("Barbarian King") + gap), end="")
        print("-" * (len("Archer Queen") if right else len("Barbarian King")))
        
        key = input_to(getch)
        n = select_hero_controls(key)
        
        if n == 101:
            right = not right
        elif n == 102:
            break
            
    return right

def select_hero_controls(key):
    if key == " ":
        return 101
    elif key == "c":
        return 102
    elif key == "q":
        end_game(0)
    
def check_game_over():
    if not len(Building.all) and not W.alive:
        end_game(1)
    if not len(Entity.all):
        end_game(0)
         
def end_game(status):
    # os.system("clear")
    if(status):
        print("█       █  █████   █    █        █           █  █████  ██       █")
        print(" █     █  ██   ██  █    █        █           █    █    █ █      █")
        print("  █   █   █     █  █    █        █           █    █    █  █     █") 
        print("   ███    █     █  █    █         █    █    █     █    █   █    █")
        print("    █     █     █  █    █         █   █ █   █     █    █    █   █")
        print("    █     ██   ██  █    █         █   █ █   █     █    █     █  █")
        print("    █      █   █   █    █          █ █   █ █      █    █      █ █")
        print("    █      █████   ██████          ███   ███    █████  █       ██")
    else:
        print("█       █  █████   █    █        █         █████    █████   ███████")
        print(" █     █  ██   ██  █    █        █        ██   ██  ██       █      ")
        print("  █   █   █     █  █    █        █        █     █  █        █      ") 
        print("   ███    █     █  █    █        █        █     █   ██      ███████")
        print("    █     █     █  █    █        █        █     █     ███   █      ")
        print("    █     ██   ██  █    █        █        ██   ██       ██  █      ")
        print("    █      █   █   █    █        █         █   █        ██  █      ")
        print("    █      █████   ██████        ██████    █████    █████   ███████")
        
    show_cursor()
    os.system("stty echo")
    
    exit()
    
def setup_walls(cannon):
    # Wall
    walls = []
    for i in range(200):
        walls.append(Building("Wall", WALL_LETTERS, WALL_COLOR, WALL_SIZE, WALL_HEALTH))
        

    # X border
    LEFT_X = th.X - 1
    RIGHT_X = th.X + th.size[0]
    
    # Y border
    TOP_Y = th.Y - 1
    BOT_Y = th.Y + th.size[1]
    
    
    def surround_townhall(i):
        # Horizontal walls
        for y in [TOP_Y, BOT_Y]:
            for x in range(LEFT_X, RIGHT_X + 1):
                walls[i].draw(x, y)
                i += 1
                
        # Vertical walls
        for x in [LEFT_X, RIGHT_X]:
            for y in range(TOP_Y, BOT_Y + 1):
                walls[i].draw(x, y)
                i += 1
                
        return i
                
    def arms(i):
        # Bottom arm
        for y in range(BOT_Y + 1, BOT_Y + 4):
            walls[i].draw(LEFT_X, y)
            i += 1
        for x in range(LEFT_X, LEFT_X + 4):
            walls[i].draw(x, BOT_Y + 3)
            i += 1
            
            
        # Top arm
        for y in range(TOP_Y - 1, TOP_Y - 4, -1):
            walls[i].draw(RIGHT_X, y)
            i += 1
        for x in range(RIGHT_X, RIGHT_X - 4, -1):
            walls[i].draw(x, TOP_Y - 3)
            i += 1
            
            
        # Left arm
        for x in range(LEFT_X, LEFT_X - 4, -1):
            walls[i].draw(x, TOP_Y)
            i += 1
        for y in range(TOP_Y, TOP_Y + 4):
            walls[i].draw(LEFT_X - 3, y)
            i += 1
            
            
        # Right arm
        for x in range(RIGHT_X, RIGHT_X + 4):
            walls[i].draw(x, BOT_Y)
            i += 1
        for y in range(BOT_Y, BOT_Y - 4, -1):
            walls[i].draw(RIGHT_X + 3, y)
            i += 1
            
        return i
            
    i = surround_townhall(0)
    i = arms(i)
                
    walls[i].draw(6, 1)
    i += 1
    walls[i].draw(6, 2)
    i += 1
    walls[i].draw(6, 3)
    i += 1
    walls[i].draw(6, 4)
    i += 1
    walls[i].draw(6, 5)
    i += 1
    walls[i].draw(5, 5)
    i += 1
    walls[i].draw(4, 5)
    i += 1
    walls[i].draw(3, 5)
    i += 1
    walls[i].draw(2, 5)
    i += 1
    walls[i].draw(1, 5)
    i += 1