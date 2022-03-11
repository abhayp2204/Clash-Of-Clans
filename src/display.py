from .variables import *
from .entity import *
from .building import *
from .spell import *

def hud(timesteps):
    k = 1 + int(K.health/150) if K.alive else 0
    Print([K.color + "King: " + str(int(K.health)) + "*"*k + " "*(int(K.max_health/150) - k)])
    
    t = 1 + int(th.health/100) if th.alive else 0
    
    Print([th.color + "  Townhall: " + "*"*t + " "*(int(th.max_health/100) - t)])
    for i in range(NUM_CANNONS):
        C = Cannon.all[i]
        c = 1 + int(C.health/100) if C.alive else 0
        Print([C.color + "   Cannon " + str(i+1) + ": " + "*"*c + " "*(int(C.max_health/100) - c)])
        
    print(Fore.YELLOW + "   Buildings: " + str(len(Building.all)), end="")
    print("   Timestep: " + str(timesteps))
    
    print(Fore.GREEN + "Heal spells: " + str(Heal.number), end="")
    print(Fore.RED + "   Rage spells: " + str(Rage.number), end="")
    print(Fore.RED + "(", end="")
    print(Fore.RED + "." if Rage.active else "", end="")
    print(Fore.RED + ")", end="")
    print()
         
def footer():
    pass
    print("Troops = ", Entity.all)
    print("Buildings = ", Building.all)
    # print("Message = ", K.message)
         
def print_canvas():
    # Use buffer to avoid flickering
    BUFFER = "\n"
    for i in range(CANVAS_HEIGHT):
        BUFFER += "".join(CANVAS[i])
        BUFFER += "\n"
    print(BUFFER)
    
def print_canvas_2():
    # Use buffer to avoid flickering
    for i in range(CANVAS_HEIGHT):
        for j in range(CANVAS_WIDTH):        
            print(CANVAS[i][j])
    print()
        
def set_border():
    # Horizontal borders
    for x in range(0, CANVAS_WIDTH):
        CANVAS[0][x] = "═"
        CANVAS[CANVAS_HEIGHT-1][x] = "═"
        
    # Vertical borders
    for y in range(0, CANVAS_HEIGHT):
        CANVAS[y][0] = "║"
        CANVAS[y][CANVAS_WIDTH-1] = "║"
        
    # Corners
    CANVAS[0][0] = "╔"
    CANVAS[0][CANVAS_WIDTH-1] = "╗"
    CANVAS[CANVAS_HEIGHT-1][0] = "╚"
    CANVAS[CANVAS_HEIGHT-1][CANVAS_WIDTH - 1] = "╝"