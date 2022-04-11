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
message = ""
BUFFER = ""
timesteps = 0

# Paths
cwd = Path.cwd()
replays = str(cwd) + "/replays"
path = str(cwd) + "/replays/replay.txt"
length = str(cwd) + "/replays/len.txt"

# Files
F = open(path, "w")
L = open(length, "w")

H = select_hero(F, L)
init(H, 1)

while (True):
    # Controls
    key = input_to(getch)
    input_handler(key, H, th.level, F, L, timesteps)
    
    # Troops and buildings
    handle_barbarians(timesteps)
    handle_archers(timesteps)
    handle_balloons(timesteps)
    handle_cannons(H, timesteps)
    handle_wizard_towers(H, timesteps)
    handle_witch(H, F, L, timesteps)
    grim_reaper()
    handle_buildings(timesteps)
    handle_aerial()
    
    if H.name == "Archer Queen" and H.active:
        if time.time() - H.time >= 1:
            H.use_eagle_arrow()
    
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
    F.write(BUFFER)
    L.write(str(len(BUFFER)) + "\n")
    
    check_game_over(H, F, L)
    footer()
    
    th.message = Building.all