from .variables import *
from .entity import *
from .util import *

def input_handler(key):
    if(key == "q"):
        end_game()
    if(key == "1"):
        if(len(Barbarian) == MAX_BARBARIANS):
            return
        
        B = Entity("Barbarian", BARBARIAN_COLOR, BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED)
        Barbarian.append(B)
    
        
def end_game():
    show_cursor()
    os.system("stty echo")
    print(Barbarian)
    exit()