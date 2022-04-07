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

    # Setup village
    set_border()
    
    # Townhall
    th.draw(int((CENTER_X - TOWNHALL_SIZE[0])/X_SCALE), CENTER_Y - int(TOWNHALL_SIZE[1]/2))  

    # Huts
    for i in range(0, NUM_HUTS):
        H = Building("Hut", HUT_LETTERS, HUT_COLOR, HUT_SIZE, HUT_HEALTH)
        H.draw(HUT_POSITIONS[i][0], HUT_POSITIONS[i][1])
        
    # Cannons
    # cannon = [Defender("Cannon",
    #                  CANNON_LETTERS,
    #                  CANNON_COLOR,
    #                  CANNON_SIZE,
    #                  CANNON_HEALTH,
    #                  CANNON_DAMAGE,
    #                  CANNON_FIRE_RATE,
    #                  CANNON_AOE,
    #                  CANNON_SPAN,
    #                  True,
    #                  False)
    #             for _ in range(0, NUM_CANNONS)]
    
    # cannon[0].draw(th.X - CANNON_SIZE[0], th.Y + 1)
    # cannon[1].draw(th.X + th.size[0], th.Y + 1)
    # cannon[2].draw(th.X + 1, th.Y - CANNON_SIZE[1] - 1)
    
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
    
    wt[0].draw(th.X - WIZARD_SIZE[0], th.Y + 1)
    wt[1].draw(th.X + th.size[0], th.Y + 1)
    wt[2].draw(th.X + 1, th.Y - WIZARD_SIZE[1] - 1)
        
    # Spawn Points
    for i in range(NUM_SPAWN_POINTS):
        P = SPAWN_POINT[i]
        x = P[0]
        y = P[1]
        CANVAS[y][x] = SPAWN_POINT_COLOR + BLOCK
        CANVAS[y][x+1] = SPAWN_POINT_COLOR + BLOCK
        
    setup_walls(wt)
    
    right = select_hero()
    H = Q if right else K
    H.draw(4, 10)
    
    B = Entity("Barbarian", BARBARIAN_LETTERS, BARBARIAN_COLOR, BARBARIAN_SIZE, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, 0, True, False)
        
    B.X = 16
    B.Y = 16
    B.move(th)
    
    
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
        print("O       O  OOOOO   O    O        O           O  OOOOO  OO       O")
        print(" O     O   O   O   O    O        O           O    O    O O      O")
        print("  O   O   O     O  O    O        O           O    O    O  O     O") 
        print("   OOO    O     O  O    O         O    O    O     O    O   O    O")
        print("    O     O     O  O    O         O   O O   O     O    O    O   O")
        print("    O      O   O   O    O         O   O O   O     O    O     O  O")
        print("    O      O   O   O    O          O O   O O      O    O      O O")
        print("    O      OOOOO   OOOOOO          OOO   OOO    OOOOO  O       OO")
    else:
        print("O       O  OOOOO   O    O        O         OOOOO    OOOOO   OOOOOOO")
        print(" O     O   O   O   O    O        O         O   O   OO       O      ")
        print("  O   O   O     O  O    O        O        O     O  O        O      ") 
        print("   OOO    O     O  O    O        O        O     O   OO      OOOOOOO")
        print("    O     O     O  O    O        O        O     O     OOO   O      ")
        print("    O      O   O   O    O        O         O   O        OO  O      ")
        print("    O      O   O   O    O        O         O   O        OO  O      ")
        print("    O      OOOOO   OOOOOO        OOOOOO    OOOOO    OOOOO   OOOOOOO")
        
    show_cursor()
    os.system("stty echo")
    
    exit()
    
def setup_walls(cannon):
    # Wall
    walls = []
    for i in range(100):
        walls.append(Building("Wall", WALL_LETTERS, WALL_COLOR, WALL_SIZE, WALL_HEALTH))

    x = cannon[0].X - 1
    y = cannon[0].Y - 1
    
    walls[0].draw(x, y)
    walls[1].draw(x+1, y)
    walls[2].draw(x+2, y)
    walls[3].draw(x+2, y-1)
    walls[4].draw(x+3, y-1)
    walls[5].draw(x+4, y-1)
    walls[6].draw(x+5, y-1)
    walls[7].draw(x+6, y-1)
    walls[8].draw(x+7, y-1)
    walls[9].draw(x+7, y)
    walls[10].draw(x+7, y+1)
    walls[11].draw(x+8, y)
    walls[12].draw(x+9, y)
    
    walls[13].draw(x, y+1)
    walls[14].draw(x, y+2)
    walls[15].draw(x, y+3)
    
    walls[16].draw(x+9, y+1)
    walls[17].draw(x+9, y+2)
    walls[18].draw(x+9, y+3)
    
    walls[16].draw(x+1, y+3)
    walls[17].draw(x+2, y+3)
    walls[18].draw(x+3, y+3)
    walls[19].draw(x+4, y+3)
    walls[20].draw(x+5, y+3)
    walls[21].draw(x+6, y+3)
    walls[22].draw(x+7, y+3)
    walls[23].draw(x+8, y+3)

    walls[24].draw(x-1, y)
    walls[25].draw(x-1, y-1)
    walls[26].draw(x-1, y-2)
    walls[27].draw(x-1, y-3)
    
    walls[28].draw(x+10, y)
    walls[29].draw(x+10, y-1)
    walls[30].draw(x+10, y-2)
    walls[31].draw(x+10, y-3)
    
    walls[32].draw(x-1, y-4)
    walls[33].draw(x+0, y-4)
    walls[34].draw(x+1, y-4)
    walls[35].draw(x+2, y-4)
    walls[36].draw(x+3, y-4)
    walls[37].draw(x+4, y-4)
    walls[38].draw(x+5, y-4)
    walls[39].draw(x+6, y-4)
    walls[40].draw(x+7, y-4)
    walls[41].draw(x+8, y-4)
    walls[42].draw(x+9, y-4)
    walls[43].draw(x+10, y-4)
    
    walls[44].draw(x-1, y+3)
    walls[45].draw(x-1, y+4)
    walls[46].draw(x-1, y+5)
    walls[47].draw(x-1, y+6)
    walls[48].draw(x, y+6)
    walls[49].draw(x+1, y+6)
    walls[50].draw(x+2, y+6)
    
    walls[51].draw(x+10, y+3)
    walls[52].draw(x+10, y+4)
    walls[53].draw(x+10, y+5)
    walls[54].draw(x+10, y+6)
    walls[55].draw(x+9, y+6)
    walls[56].draw(x+8, y+6)
    walls[57].draw(x+7, y+6)
    
    walls[58].draw(5, 1)
    walls[59].draw(5, 2)
    walls[60].draw(5, 3)
    walls[61].draw(5, 4)
    walls[62].draw(4, 4)
    walls[63].draw(3, 4)
    walls[64].draw(2, 4)
    walls[65].draw(1, 4)
    # walls[66].draw(5, 3)