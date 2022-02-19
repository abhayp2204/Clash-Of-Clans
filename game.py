# General imports
import numpy as np
import colorama
from colorama import Fore, Back, Style

# Classes
from entity import *
from building import *

# Misc
from stats import *

# Color codes don't work on Windows without this command
# Autoresest: Avoid clearing color everytime
colorama.init(autoreset=True)

print(Entity.all)