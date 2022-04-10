from .variables import *
from .entity import *
from .building import *
from .spell import *
from .setup import *

def hud(H, timesteps):
    BUFFER = ""
    
    hu = 800
    k = 1 + int(H.health/hu) if H.alive else 0
    BUFFER += Fore.BLUE + H.name + ": " + str(int(H.health)) + "*"*k + " "*(int(H.max_health/hu) - k)
    
    hu = 120
    t = 1 + int(th.health/hu) if th.alive else 0
    
    if th.alive:
        BUFFER += Fore.MAGENTA + "  Townhall: " + "*"*t + " "*(int(th.max_health/hu) - t)
    else:
        hu = 100
        w = 1 + int(W.health/hu) if W.alive else 0
        BUFFER += Fore.GREEN + "Witch: " + str(int(W.health)) + "*"*w + " "*(int(W.max_health/hu) - w)
        
    BUFFER += Fore.YELLOW + "   Buildings: " + str(len(Building.all))
    BUFFER += Fore.WHITE + "   Level: " + str(th.level)
    BUFFER += Fore.GREEN + "\nHeal spells: " + str(Heal.number)
    
    BUFFER += Fore.RED + "   Rage spells: " + str(Rage.number)
    BUFFER += Fore.RED + "("
    BUFFER += Fore.RED + "." if Rage.active else ""
    BUFFER += Fore.RED + ")"
    
    BUFFER += Fore.WHITE + "   Timestep: " + str(timesteps)
    return BUFFER
         
def footer():
    pass
    # print("Troops = ", Entity.all)
    print("Buildings = ", Building.all)
    # print("Message = ", th.health)
         
def get_canvas(BUFFER):
    # Use buffer to avoid flickering
    BUFFER += "\n"
    for i in range(CANVAS_HEIGHT):
        BUFFER += "".join(CANVAS[i])
        BUFFER += "\n"
    return BUFFER
        
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
    CANVAS[0][0] = Fore.WHITE + "╔"
    CANVAS[0][CANVAS_WIDTH-1] = Fore.WHITE + "╗"
    CANVAS[CANVAS_HEIGHT-1][0] = Fore.WHITE + "╚"
    CANVAS[CANVAS_HEIGHT-1][CANVAS_WIDTH - 1] = Fore.WHITE + "╝"