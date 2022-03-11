# Classes
from src.entity import *
from src.building import *

# Misc
from src.variables import *
from src.setup import *
from src.main import *
from src.display import *
from src.controls import *
from src.util import *
from src.input import *
from src.stats import *

START_TIME = time.time()
getch = Get()
init()
message = ""
BUFFER = ""
timesteps = 0

while (True):
    key = input_to(getch)
    input_handler(key, timesteps)
    
    # Rage spell wears off
    if(timesteps > Rage.time + Rage.duration):
        Rage.reset()
    
    handle_barbarians(timesteps)
    handle_cannons(timesteps)
    handle_buildings(timesteps)
    handle_witch(timesteps)
    grim_reaper()
    
    current_time = time.time()
    seconds = current_time - START_TIME
    timesteps = int(seconds / TIMESTEP)
    
    # Display
    os.system("clear")
    hud(timesteps)
    print_canvas()
    check_game_over()
    footer()
    
# Exit
print()
show_cursor()
os.system("stty echo")