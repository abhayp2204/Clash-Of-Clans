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

while (not game_over):
    # break

    key = input_to(getch)
    input_handler(key)
    
    handle_barbarians(timesteps)
    handle_cannons(timesteps)
    grim_reaper()
    
    if(game_over):
        break
    
    current_time = time.time()
    seconds = current_time - START_TIME
    timesteps = int(seconds / TIMESTEP)
    
    # Display
    os.system("clear")
    hud(timesteps)
    print_canvas()
    footer()
    
# Exit
print()
show_cursor()
os.system("stty echo")