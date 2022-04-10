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
H = select_hero()
init(H, 1)
message = ""
BUFFER = ""
timesteps = 0

print(Fore.RED + Back.WHITE + "K")

while (True):
    # Controls
    key = input_to(getch)
    input_handler(key, H, th.level, timesteps)
    
    # Troops and buildings
    handle_barbarians(timesteps)
    handle_archers(timesteps)
    handle_balloons(timesteps)
    handle_cannons(H, timesteps)
    handle_wizard_towers(H, timesteps)
    handle_witch(H, timesteps)
    grim_reaper()
    handle_buildings(timesteps)
    handle_aerial()
    
    
    # Timesteps
    current_time = time.time()
    seconds = current_time - START_TIME
    timesteps = int(seconds / TIMESTEP)
    
    
    # Rage spell wears off
    if(timesteps > Rage.time + Rage.duration):
        Rage.reset()
        
    
    # Display
    os.system("clear")
    BUFFER = hud(H, timesteps)
    BUFFER = get_canvas(BUFFER)
    print(BUFFER)
    check_game_over(H)
    footer()
    
    th.message = Building.all