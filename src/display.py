from .variables import *
from .entity import *
from .building import *
from .spell import *

def hud(timesteps):
    BUFFER = ""
    
    hu = 400
    k = 1 + int(K.health/hu) if K.alive else 0
    Print([K.color + "King: " + str(int(K.health)) + "*"*k + " "*(int(K.max_health/hu) - k)])
    
    t = 1 + int(th.health/100) if th.alive else 0
    
    if th.alive:
        Print([th.color + "  Townhall: " + "*"*t + " "*(int(th.max_health/100) - t)])
    else:
        hu = 100
        w = 1 + int(W.health/hu) if W.alive else 0
        Print([Fore.GREEN + "Witch: " + str(int(W.health)) + "*"*w + " "*(int(W.max_health/hu) - w)])
        
    for i in range(NUM_CANNONS):
        C = Cannon.all[i]
        c = 1 + int(C.health/100) if C.alive else 0
        Print([C.color + "   Cannon " + str(i+1) + ": " + "*"*c + " "*(int(C.max_health/100) - c)])
        
    BUFFER += Fore.YELLOW + "\nBuildings: " + str(len(Building.all))
    BUFFER += Fore.WHITE + "   Timestep: " + str(timesteps) + "\n"
    BUFFER += Fore.GREEN + "Heal spells: " + str(Heal.number)
    BUFFER += Fore.RED + "   Rage spells: " + str(Rage.number)
    BUFFER += Fore.RED + "("
    BUFFER += Fore.RED + "." if Rage.active else ""
    BUFFER += Fore.RED + ")"
    print(BUFFER)
         
def footer():
    pass
    # print("Troops = ", Entity.all)
    # print("Buildings = ", Building.all)
    # print("Message = ", th.message)
         
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