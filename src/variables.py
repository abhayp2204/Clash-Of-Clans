import os
import time
import random
import colorama
import numpy as np
from colorama import Fore, Back, Style

# King
KING_COLOR = Fore.RED
KING_HEALTH = 7500
KING_DAMAGE = 100
KING_SPEED = 1
KING_AXE_DAMAGE = 40
KING_AXE_AREA = 5

# Barbarian
BARBARIAN_COLOR = Fore.YELLOW
BARBARIAN_ATTACK_COLOR = Fore.RED
BARBARIAN_HEALTH = 100
BARBARIAN_DAMAGE = 10
BARBARIAN_SPEED = 4
MAX_BARBARIANS = 10

# Townhall
TOWNHALL_SIZE = (4, 3)
TOWNHALL_COLOR = Fore.MAGENTA
TOWNHALL_HEALTH = 1000

# Huts
NUM_HUTS = 1
HUT_SIZE = (1, 1)
HUT_COLOR = Fore.GREEN
HUT_HEALTH = 120

# Cannons
NUM_CANNONS = 2
CANNON_SIZE = (2, 2)
CANNON_HEALTH = 350
CANNON_COLOR = Fore.BLUE
CANNON_DAMAGE = 8
CANNON_FIRE_RATE = 0.5
CANNON_SPAN = 8

# Canvas
CANVAS_WIDTH = 114
CANVAS_HEIGHT = 34
CENTER_X = 57
CENTER_Y = 17
MOVE_CURSOR = "\033[%d;%dH"
Print = lambda content: print(*content, sep='', end='', flush=True)
LINES = [True for _ in range(CANVAS_HEIGHT)]
CANVAS = [[" "]*CANVAS_WIDTH for _ in range(CANVAS_HEIGHT)]

# Spawing points
NUM_SPAWN_POINTS = 3
SPAWN_POINT_COLOR = Fore.WHITE
SPAWN_POINT_A = (2, 1)
SPAWN_POINT_B = (CANVAS_WIDTH - 4, 1)
SPAWN_POINT_C = (2, CANVAS_HEIGHT - 2)
SPAWN_POINT = [SPAWN_POINT_A, SPAWN_POINT_B, SPAWN_POINT_C]

game_over = False
Barbarian = []
TIMESTEP = 0.5
timesteps = 0

# Directions
NORTH = 101
EAST = 102
WEST = 103
SOUTH = 104