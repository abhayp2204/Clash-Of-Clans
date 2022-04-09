from .display import *
from .variables import *
from .input import *
from .util import *

def init(H, level):
    # Color codes don't work on Windows without this command
    # Autoreset: Avoid clearing color everytime
    colorama.init(autoreset=True)

    # Setup terminal
    os.system("clear")
    os.system("stty -echo")
    hide_cursor()
    
    # Setup village
    set_border()
    
    # Townhall
    th.draw(int((CENTER_X - TOWNHALL_SIZE[0])/X_SCALE), CENTER_Y - int(TOWNHALL_SIZE[1]/2))  

    # Huts
    if(level == 1):
        for i in range(0, NUM_HUTS):
            Ht = Building("Hut", HUT_LETTERS, HUT_COLOR, HUT_SIZE, HUT_HEALTH)
            Ht.draw(HUT_POSITIONS[i][0], HUT_POSITIONS[i][1])
            
    if(level == 2):
        for Ht in Building.huts:
            Ht.X = 4
            Ht.Y = 12
        
    # Wizard Towers
    for i in range(0, len(WIZARD_POSITIONS[th.level - 1])):
        W = Defender("Wizard Tower",
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
        W.draw(WIZARD_POSITIONS[th.level - 1][i][0], WIZARD_POSITIONS[th.level - 1][i][1])
        
    # Cannons
    for i in range(0, len(CANNON_POSITIONS[th.level - 1])):
        C = Defender("Cannon",
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
        C.draw(CANNON_POSITIONS[th.level - 1][i][0], CANNON_POSITIONS[th.level - 1][i][1])
        
    # Gold Storage
    for i in range(0, len(GOLD_POSITIONS[th.level - 1])):
        C = Building("Gold",
                    GOLD_LETTERS,
                    GOLD_COLOR,
                    GOLD_SIZE,
                    GOLD_HEALTH)
        C.draw(GOLD_POSITIONS[th.level - 1][i][0], GOLD_POSITIONS[th.level - 1][i][1])
        
    # Spawn Points
    for i in range(NUM_SPAWN_POINTS):
        P = SPAWN_POINT[i]
        x = P[0]
        y = P[1]
        
        for i in range(X_SCALE):
            CANVAS[y][x+i] = SPAWN_POINT_COLOR + Fore.WHITE + SPAWN_POINT_LETTERS[i] + Back.RESET
    
    setup_walls(th.level)
    
    H.draw(4, 10)
    H.health = H.max_health

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
        print(Fore.RED + "Barbarian King" + " "*gap + Fore.MAGENTA + "Archer Queen" + Fore.RESET)
        if right:
            print(" "*(len("Barbarian King") + gap), end="")
        print("-" * (len("Archer Queen") if right else len("Barbarian King")))
        
        key = input_to(getch)
        if not key is None:
            key = key.lower()
        n = select_hero_controls(key)
        
        if n == 101:
            right = not right
        elif n == 102:
            break
        
    H = Q if right else K
    return H

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
    
def setup_walls(level):
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
            
    def surround_spawn_point_1(i): 
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

    i = surround_townhall(0)
    
    if level == 1:
        i = arms(i)
        i = surround_spawn_point_1(i)

                
                
                
    