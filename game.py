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
H = init()
message = ""
BUFFER = ""
timesteps = 0

print(Fore.RED + Back.WHITE + "K")
# end_game(1)

while (True):
    key = input_to(getch)
    input_handler(key, H, timesteps)
    
    # Rage spell wears off
    if(timesteps > Rage.time + Rage.duration):
        Rage.reset()
    
    handle_barbarians(timesteps)
    handle_archers(timesteps)
    handle_balloons(timesteps)
    handle_cannons(timesteps)
    handle_wizard_towers(timesteps)
    handle_buildings(timesteps)
    handle_witch(timesteps)
    grim_reaper()
    
    current_time = time.time()
    seconds = current_time - START_TIME
    timesteps = int(seconds / TIMESTEP)
    # th.message = Entity.all[3].health
    
    # Display
    os.system("clear")
    BUFFER = hud(H, timesteps)
    BUFFER = get_canvas(BUFFER)
    print(BUFFER)
    check_game_over()
    footer()
    
# Exit
print()
show_cursor()
os.system("stty echo")