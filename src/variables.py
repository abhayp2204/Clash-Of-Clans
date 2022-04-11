import os
import time
import random
import colorama
import math
import numpy as np
from pathlib import Path
from colorama import Fore, Back, Style

# King
KING_LETTERS = "BK"
KING_COLOR = Back.BLUE
KING_BGCOLOR = Back.BLUE
KING_SIZE = (1, 1)
KING_HEALTH = 5000
KING_DAMAGE = 160
KING_SPEED = 1
KING_AXE_DAMAGE = 60
KING_AXE_AREA = 5
KING_NUM_POWER_ATTACK = 3

# Queen
QUEEN_LETTERS = "AQ"
QUEEN_COLOR = Back.CYAN
QUEEN_BGCOLOR = Back.BLUE
QUEEN_SIZE = (1, 1)
QUEEN_HEALTH = 2500
QUEEN_DAMAGE = int(KING_DAMAGE / 4)
QUEEN_AOE = 5
QUEEN_ARROW_DISTANCE = 8
QUEEN_EAGLE_AOE = 9
QUEEN_EAGLE_ARROW_DISTANCE = 16
QUEEN_SPEED = KING_SPEED
QUEEN_NUM_POWER_ATTACK = 3
QUEEN_POWER_ATTACK_TIME = 1

# Barbarian
BARBARIAN_LETTERS = "Br"
BARBARIAN_COLOR = Back.RED
BARBARIAN_SIZE = (1, 1)
BARBARIAN_HEALTH = 2000
BARBARIAN_DAMAGE = 80
BARBARIAN_SPEED = 1
MAX_BARBARIANS = [6, 8, 10]

# Archer
ARCHER_LETTERS = "Ar"
ARCHER_COLOR = Back.MAGENTA
ARCHER_SIZE = (1, 1)
ARCHER_HEALTH = int(BARBARIAN_HEALTH/2)
ARCHER_DAMAGE = int(BARBARIAN_DAMAGE/2)
ARCHER_SPEED = BARBARIAN_SPEED * 2
ARCHER_RANGE = 25
MAX_ARCHERS = [6, 8, 10]

# Balloons
BALLOON_LETTERS = "Bl"
BALLOON_COLOR = Back.BLACK
BALLOON_SIZE = (1, 1)
BALLOON_HEALTH = BARBARIAN_HEALTH
BALLOON_DAMAGE = BARBARIAN_DAMAGE * 2
BALLOON_SPEED = BARBARIAN_SPEED * 2
BALLOON_LAND = False
BALLOON_AIR = True
MAX_BALLOONS = [3, 5, 8]

# Witch
WITCH_LETTERS = "Wc"
WITCH_COLOR = Fore.MAGENTA
WITCH_SIZE = (1, 1)
WITCH_HEALTH = 400
WITCH_DAMAGE = 300
WITCH_SPEED = 1

# Townhall
TOWNHALL_LETTERS = "Townhall"
TOWNHALL_SIZE = (4, 3)
TOWNHALL_COLOR = Back.MAGENTA
TOWNHALL_HEALTH = 1000

# Huts
HUT_LETTERS = "Ht"
HUT_SIZE = (1, 1)
HUT_COLOR = Back.GREEN
HUT_HEALTH = 300
HUT_POSITIONS = [
    # Level 1
    [
        (16, 10),
        (15, 18),
        (23, 18),
        (24, 10),
        (19, 7),
        (20, 21)
    ],
    # Level 2
    [
        (18, 7),
        (21, 7),
        (18, 21),
        (21, 21),
        (12, 11),
        (12, 17),
        (27, 11),
        (27, 17),
    ],
    # Level 3
    [
        (20, 7),
        (24, 7),
        (15, 21),
        (19, 21),
        (12, 10),
        (12, 14),
        (27, 14),
        (27, 18),
    ]
]
NUM_HUTS = len(HUT_POSITIONS)

# Gold Storage
GOLD_LETTERS = "Gold"
GOLD_NUM = 4
GOLD_SIZE = (2, 2)
GOLD_COLOR = Back.YELLOW
GOLD_HEALTH = 3000
GOLD_POSITIONS = [
    # Level 1
    [
        (18, 10),
        (20, 17),
        (15, 15),
        (23, 12)
    ],
    # Level 2
    [
        (16, 10),
        (22, 10),
        (16, 17),
        (22, 17)
    ],
    # Level 3
    [
        (18, 10),
        (20, 17),
        (15, 15),
        (23, 12)
    ]
]

# Cannons
CANNON_LETTERS = "Cann"
CANNON_NUM = 2
CANNON_SIZE = (2, 2)
CANNON_HEALTH = 2000
CANNON_COLOR = Back.RED
CANNON_DAMAGE = 50
CANNON_FIRE_RATE = 0.5
CANNON_SPAN = 5
CANNON_AOE = 0
CANNON_POSITIONS = [
    # Level 1
    [
        (15, 13),
        (23, 14)
    ],
    # Level 2
    [
        (19, 10),
        (23, 15),
        (15, 15)
    ],
    # Level 3
    [
        (16, 10),
        (15, 17),
        (22, 17),
        (23, 10),
    ]
]

# Wizard Tower
WIZARD_LETTERS = "WzTw"
WIZARD_NUM = 2
WIZARD_SIZE = (2, 2)
WIZARD_HEALTH = 1400
WIZARD_COLOR = Back.CYAN
WIZARD_DAMAGE = CANNON_DAMAGE
WIZARD_FIRE_RATE = 0.5
WIZARD_SPAN = 5
WIZARD_AOE = 3
WIZARD_POSITIONS = [
    # Level 1
    [
        (18, 17),
        (20, 10)
    ],
    # Level 2
    [
        (19, 17),
        (15, 12),
        (23, 12)
    ],
    # Level 3
    [
        (18, 17),
        (20, 10),
        (15, 13),
        (23, 14)
    ]
]

# WALL
WALL_LETTERS = ""
WALL_SIZE = (1, 1)
WALL_HEALTH = 25
WALL_COLOR = Fore.WHITE

# Rage Spell
NUM_RAGE_SPELLS = 3
RAGE_HEALTH_BUFF = 1
RAGE_DAMAGE_BUFF = 2
RAGE_SPEED_BUFF = 2
RAGE_DURATION = 400

# Heal Spell
NUM_HEAL_SPELLS = 2
HEAL_HEALTH_BUFF = 1.5
HEAL_DAMAGE_BUFF = 1
HEAL_SPEED_BUFF = 1

# Canvas
CANVAS_WIDTH = 80
CANVAS_HEIGHT = 29

CENTER_X = int(CANVAS_WIDTH/2)
CENTER_Y = int(CANVAS_HEIGHT/2)

CANVAS = [[" "]*CANVAS_WIDTH for _ in range(CANVAS_HEIGHT)]
CINDER_BLOCK = "█"
BLOCK = CINDER_BLOCK
X_SCALE = 2

PREV = [" "]
PREV_BUILDING = []
PREV_X = [0]
PREV_Y = [0]

# Spawing points
NUM_SPAWN_POINTS = 3
SPAWN_POINT_LETTERS = "◖◗"
SPAWN_POINT_COLOR = Back.BLACK
SPAWN_POINT_A = (2, 1)
SPAWN_POINT_B = (CANVAS_WIDTH - 4, 2)
SPAWN_POINT_C = (2, CANVAS_HEIGHT - 2)
SPAWN_POINT = [SPAWN_POINT_A, SPAWN_POINT_B, SPAWN_POINT_C]

TIMESTEP = 0.01
message = ""

# Directions
NORTH = 101
EAST = 102
WEST = 103
SOUTH = 104