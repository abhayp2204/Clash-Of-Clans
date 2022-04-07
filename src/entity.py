from http.client import RESET_CONTENT
from .variables import *
from .building import *
from .util import *

class Entity:
    # List of all entities
    all = []
    Barbarians = []
    Archers = []
    Balloons = []
    
    # Class attributes
    damage_rate = 1.0
    health_rate = 1.5
        
    # __init__ is a magic method that gets called whenever an instance is created
    def __init__(self, name: str, letters, color, size, max_health, damage, speed, land, air):    
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        assert damage >= 0, f"Damage {damage} must be >= 0"
        assert speed >= 0, f"Damage {damage} must be >= 0"
        
        # Initialize
        self.name = name
        self.letters = letters
        self.color = color
        self.size = size
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.speed = speed
        self.land = land
        self.air = air
        self.alive = True
        self.target_wall = th
        self.clearing_path = False
        
        self.move_time = 0
        self.attack_time = 0
        self.message = ""
        self.killed = False
        
        self.X = 0
        self.Y = 9
        
        # Add to list of entities
        Entity.all.append(self)
        
        if(name == "Barbarian"):
            Entity.Barbarians.append(self)
        elif(name == "Archer"):
            Entity.Archers.append(self)
        elif(name == "Balloon"):
            Entity.Balloons.append(self)

    def draw(self, posX, posY): 
        if(X_SCALE*(posX + self.size[0]) >= CANVAS_WIDTH):
            return
        if(posY + self.size[1] >= CANVAS_HEIGHT):
            return
        
        self.X = posX*X_SCALE
        self.Y = posY
                
        # char = (self.color + BLOCK) if self.alive else " "
        for i in range(self.size[0]*X_SCALE):
            char = KING_BGCOLOR + Fore.BLACK + self.letters[i] + Back.RESET
            CANVAS[self.Y][self.X + i] = char
                
    def erase(self):
        CANVAS[self.Y][self.X] = " "
        CANVAS[self.Y][self.X + 1] = " "

    def move(self, target):
        # Move = Erase -> Change Location -> Redraw
        def erase():
            for i in range(X_SCALE):
                CANVAS[self.Y][self.X + i] = " "
        def redraw():
            for i in range(X_SCALE):
                if(self.name == "Balloon"):
                    CANVAS[self.Y][self.X + i] = self.color + Fore.WHITE + self.letters[i] + Back.RESET
                    continue
                CANVAS[self.Y][self.X + i] = self.color + Fore.BLACK + self.letters[i] + Back.RESET
            
        def move_up():
            erase()
            self.Y -= 1
            redraw()
        def move_down():
            erase()
            self.Y += 1
            redraw()  
        def move_left():
            erase()
            self.X -= X_SCALE
            redraw() 
        def move_right():
            erase()
            self.X += X_SCALE
            redraw()
        
        # Entity destroys the wall it was attacking
        if(not self.target_wall.alive):
            self.clearing_path = False
            
        # Redraw the block under aerial troops
        if self.air:
            if len(PREV_BUILDING):
                b = PREV_BUILDING[0]
                if b.alive:
                    for i in range(len(PREV)):
                        for x in range(X_SCALE):
                            CANVAS[b.Y][b.X + x] = PREV[i]
            
        # Targeting a Building
        if(self != W):
            if(target.X * X_SCALE > self.X):    
                ch = CANVAS[self.Y][self.X + X_SCALE]
                if self.air:
                    move_right()
                    
                    # Keep track of the block under aerial troops
                    PREV.append(ch)
                    PREV_X.append(self.X)
                    PREV_Y.append(self.Y)
                else:
                    if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                        move_right()
            elif(target.X * X_SCALE < self.X):
                ch = CANVAS[self.Y][self.X - X_SCALE]
                if self.air:
                    move_left()
                else:
                    if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                        move_left()
                    
            for b in Building.all:
                if b.X == int(self.X/2) and b.Y == self.Y - 1:
                    PREV_BUILDING.append(b)
                    
        # Targetting an Entity
        else:
            if(target.X > self.X):
                ch = CANVAS[self.Y][self.X + X_SCALE]
                if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                    move_right()
            elif(target.X < self.X):
                ch = CANVAS[self.Y][self.X - X_SCALE]
                if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                    move_left()
                
        # Targetting Building or Entity
        if(target.Y > self.Y):
            ch = CANVAS[self.Y + 1][self.X]
            if self.air:
                move_down()
                
                # Keep track of the block under aerial troops
                PREV.append(ch)
                PREV_X.append(self.X)
                PREV_Y.append(self.Y)
            else:         
                if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                    move_down()
        elif(target.Y < self.Y):
            ch = CANVAS[self.Y - 1][self.X]
            if self.air:
                move_up()
                
                # Keep track of the block under aerial troops
                PREV.append(ch)
                PREV_X.append(self.X)
                PREV_Y.append(self.Y)
            else:
                if(ch == " " or ch == BARBARIAN_COLOR + BLOCK):
                    move_up()
                
        if(self.name == "Balloon"):
            return
                
        # If a wall is the way, set that wall as the target
        if(target.X * X_SCALE > self.X): 
            if(ch == WALL_COLOR + BLOCK):
                for w in Building.walls:
                    if(self.Y == w.Y and self.X + X_SCALE == w.X * X_SCALE):
                        self.target_wall = w
                        self.clearing_path = True
                        return
        elif(target.X*X_SCALE < self.X): 
            if(ch == WALL_COLOR + BLOCK):
                for w in Building.walls:
                    if(self.Y == w.Y and self.X - X_SCALE == w.X * X_SCALE):
                        self.target_wall = w
                        self.clearing_path = True
                        return
            
        
        if(target.Y > self.Y):
            if(ch == WALL_COLOR + BLOCK):
                for w in Building.walls:
                    if(self.Y + 1 == w.Y and self.X == w.X*X_SCALE):
                        self.target_wall = w
                        self.clearing_path = True
                        return
        elif(target.Y < self.Y):
            if(ch == WALL_COLOR + BLOCK):
                for w in Building.walls:
                    if(self.Y - 1 == w.Y and self.X== w.X*X_SCALE):
                        self.target_wall = w
                        self.clearing_path = True
                        return
    
    def within_attack_range(self, target):
        if not target.alive:
            return
        
        dx = int((target.X - self.X/X_SCALE))
        if(self == W):
            dx = int((target.X - self.X)/X_SCALE)
            
        dy = (target.Y - self.Y)
        
        if(self.name == "Archer"):
            self.damage = ARCHER_DAMAGE
            dist = dx**2 + dy**2
            
            if(dist < 100):
                return True
            
        if(self.name == "Balloon"):
            if (dx <= 0 and dx > -target.size[0]) and (dy <= 0 and dy > -target.size[1]):
                return True
            else:
                return False
            
        
        # Far
        if(dx > 1 or dx < -target.size[0] or dy > 1 or dy < -target.size[1]):
            return False
        
        dx = abs(dx)
        dy = abs(dy)
        
        # Diagonal
        if(dx == 1 and dy == 1):
            return False
        
        return True

    def attack(self, target):
        if not target.alive:
            return
        target.health -= self.damage
            
    def apply_rage_spell(self):
        self.damage *= 2
        self.speed *= 2
        
    def apply_heal_spell(self):
        self.health *= 1.5
        # Cap at max health
        if(self.health > self.max_health):
            self.health = self.max_health

    # Customized representation of the object
    def __repr__(self):
        return f"{self.name}"
    
class King(Entity):
    def __init__(self, name: str, letters, color, size, max_health, damage, speed, land, air, axe_damage, axe_area):
        # Inherit
        super().__init__(name, letters, color, size, max_health, damage, speed, land, air)
        
        # Validate
        assert axe_damage > 0, f"Damage {axe_damage} must be > 0"
        assert axe_area > 0, f"Fire Rate {axe_area} must be > 0"
        
        # Initialize
        self.health = max_health
        self.axe_damage = axe_damage
        self.axe_area = axe_area
        self.direction = EAST
        
    def clear(self):
        for i in range(X_SCALE):
            CANVAS[self.Y][self.X + i] = " "
                
    def paint(self):
        for i in range(X_SCALE):
            CANVAS[self.Y][self.X + i] = Back.BLUE + Fore.BLACK + self.letters[i] + Back.RESET
        
    def move_up(self):
        if not self.alive:
            return
        
        self.direction = NORTH
        if(CANVAS[self.Y - 1][self.X] != " "):
            return False
                  
        self.clear()
        self.Y -= 1
        self.paint()
        
        return True
        
    def move_left(self):
        if not self.alive:
            return
        
        self.direction = WEST
        
        for i in range(X_SCALE):
            if(CANVAS[self.Y][self.X - i - 1] != " "):
                return False
        
        self.clear()
        self.X -= X_SCALE
        self.paint()
        
        return True
        
    def move_down(self):
        if not self.alive:
            return
        
        self.direction = SOUTH
        if(CANVAS[self.Y + 1][self.X] != " "):
            return False
        
        self.clear()
        self.Y += 1
        self.paint()
        
        return True
        
    def move_right(self):
        if not self.alive:
            return
        
        self.direction = EAST
        if(CANVAS[self.Y][self.X + X_SCALE*2 - 1] != " "):
            return False
        
        self.clear()
        self.X += X_SCALE
        self.paint()
        
        return True
        
    def attack(self):
        if(self.direction == NORTH):
            ch = CANVAS[self.Y - 1][self.X]
            if(ch != " "):
                for building in Building.all:
                    if not(self.X >= building.X * X_SCALE and self.X < (building.X + building.size[0]) * X_SCALE):
                        continue
                    if(self.Y == building.Y + building.size[1]):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.X >= w.X * X_SCALE and self.X < (w.X + w.size[0]) * X_SCALE):
                        continue
                    if(self.Y == w.Y + w.size[1]):
                        w.health -= KING_DAMAGE

        if(self.direction == SOUTH):
            ch = CANVAS[self.Y + 1][self.X]
            if(ch != " "):
                for building in Building.all:
                    if not(self.X >= building.X * X_SCALE and self.X < (building.X + building.size[0])* X_SCALE):
                        continue
                    if(self.Y + 1 == building.Y):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.X >= w.X * X_SCALE and self.X < (w.X + w.size[0]) * X_SCALE):
                        continue
                    if(self.Y + 1 == w.Y):
                        w.health -= KING_DAMAGE
                        
        if(self.direction == EAST):
            ch = CANVAS[self.Y][self.X + X_SCALE]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X + X_SCALE == building.X*X_SCALE):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.Y == w.Y):
                        continue
                    if(self.X + X_SCALE == w.X*X_SCALE):
                        w.health -= KING_DAMAGE
                        
        if(self.direction == WEST):
            ch = CANVAS[self.Y][self.X - X_SCALE]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X == building.X*X_SCALE + building.size[0]*X_SCALE):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.Y >= w.Y and self.Y < (w.Y + w.size[1])*2):
                        continue
                    if(self.X == w.X*2 + w.size[0]*X_SCALE):
                        w.health -= KING_DAMAGE
                
    def use_leviathan_axe(self):
        for b in Building.all:
            x_pass = False
            y_pass = False
            
            if((b.X - int(self.X/2) >= 0 and b.X - int(self.X/2) <= KING_AXE_AREA) or (int(self.X/2) - b.X > 0 and int(self.X/2) - b.X <= KING_AXE_AREA + b.size[0])):
                x_pass = True
            if((b.Y - self.Y >= 0 and b.Y - self.Y <= KING_AXE_AREA) or (self.Y - b.Y > 0 and self.Y - b.Y <= KING_AXE_AREA + b.size[1])):
                y_pass = True
            
            if(x_pass and y_pass):
                b.health -= KING_AXE_DAMAGE
                
        for b in Building.walls:
            x_pass = False
            y_pass = False
            
            if((b.X - int(self.X/2) >= 0 and b.X - int(self.X/2) <= KING_AXE_AREA) or (int(self.X/2) - b.X > 0 and int(self.X/2) - b.X <= KING_AXE_AREA + b.size[0])):
                x_pass = True
            if((b.Y - self.Y >= 0 and b.Y - self.Y <= KING_AXE_AREA) or (self.Y - b.Y > 0 and self.Y - b.Y <= KING_AXE_AREA + b.size[1])):
                y_pass = True
            
            if(x_pass and y_pass):
                b.health -= KING_AXE_DAMAGE

        if(W.alive):
            W.health -= KING_AXE_DAMAGE
            if(W.health <= 0):
                W.killed = True
                untrap()
                
class Queen(Entity):
    def __init__(self, name: str, letters, color, size, max_health, damage, speed, land, air, aoe, arrow_distance):
        # Inherit
        super().__init__(name, letters, color, size, max_health, damage, speed, land, air)
        
        # Validate
        assert aoe > 0, f"Damage {aoe} must be > 0"
        assert arrow_distance > 0, f"Fire Rate {arrow_distance} must be > 0"
        
        # Initialize
        self.health = max_health
        self.aoe = aoe
        self.arrow_distance = arrow_distance
        self.direction = EAST
        
    def clear(self):
        for i in range(X_SCALE):
            CANVAS[self.Y][self.X + i] = " "
                
    def paint(self):
        for i in range(X_SCALE):
            CANVAS[self.Y][self.X + i] = Back.BLUE + Fore.BLACK + self.letters[i] + Back.RESET
        
    def move_up(self):
        if not self.alive:
            return
        
        self.direction = NORTH
        if(CANVAS[self.Y - 1][self.X] != " "):
            return False
                  
        self.clear()
        self.Y -= 1
        self.paint()
        
        return True
        
    def move_left(self):
        if not self.alive:
            return
        
        self.direction = WEST
        
        for i in range(X_SCALE):
            if(CANVAS[self.Y][self.X - i - 1] != " "):
                return False
        
        self.clear()
        self.X -= X_SCALE
        self.paint()
        
        return True
        
    def move_down(self):
        if not self.alive:
            return
        
        self.direction = SOUTH
        if(CANVAS[self.Y + 1][self.X] != " "):
            return False
        
        self.clear()
        self.Y += 1
        self.paint()
        
        return True
        
    def move_right(self):
        if not self.alive:
            return
        
        self.direction = EAST
        if(CANVAS[self.Y][self.X + X_SCALE*2 - 1] != " "):
            return False
        
        self.clear()
        self.X += X_SCALE
        self.paint()
        
        return True
        
    def attack(self):
        if(self.direction == NORTH):
            target_X = self.X
            target_Y = self.Y - self.arrow_distance
            
            half = int(self.aoe / 2)
            
            for y in range(target_Y - half, target_Y + half + 1):
                for x in range(target_X - half*X_SCALE, target_X + half*X_SCALE + 1):
                    for i in range(X_SCALE):
                        # CANVAS[y][x + i] = BLOCK
                        for B in Building.all:
                            if B.contains_cell(x, y):
                                B.health -= QUEEN_DAMAGE

        if(self.direction == SOUTH):
            target_X = self.X
            target_Y = self.Y + self.arrow_distance
            
            half = int(self.aoe / 2)
            
            for y in range(target_Y - half, target_Y + half + 1):
                for x in range(target_X - half*X_SCALE, target_X + half*X_SCALE + 1):
                    for i in range(X_SCALE):
                        # CANVAS[y][x + i] = BLOCK
                        for B in Building.all:
                            if B.contains_cell(x, y):
                                B.health -= QUEEN_DAMAGE
                        
        if(self.direction == EAST):
            target_X = self.X + (self.arrow_distance * X_SCALE)
            target_Y = self.Y
            
            half = int(self.aoe / 2)
            
            for y in range(target_Y - half, target_Y + half + 1):
                for x in range(target_X - half*X_SCALE, target_X + half*X_SCALE + 1):
                    for i in range(X_SCALE):
                        # CANVAS[y][x + i] = BLOCK
                        for B in Building.all:
                            if B.contains_cell(x, y):
                                B.health -= QUEEN_DAMAGE/2
                        
        if(self.direction == WEST):
            target_X = self.X - (self.arrow_distance * X_SCALE)
            target_Y = self.Y
            
            half = int(self.aoe / 2)
            
            for y in range(target_Y - half, target_Y + half + 1):
                for x in range(target_X - half*X_SCALE, target_X + half*X_SCALE + 1):
                    for i in range(X_SCALE):
                        # CANVAS[y][x + i] = BLOCK
                        for B in Building.all:
                            if B.contains_cell(x, y):
                                B.health -= QUEEN_DAMAGE
                                
                                
    
K = King("Barbarian King",
         KING_LETTERS,
         KING_COLOR,
         KING_SIZE,
         KING_HEALTH,
         KING_DAMAGE,
         KING_SPEED,
         True,
         False,
         KING_AXE_DAMAGE,
         KING_AXE_AREA)


Q = Queen("Archer Queen",
         QUEEN_LETTERS,
         QUEEN_COLOR,
         QUEEN_SIZE,
         QUEEN_HEALTH,
         QUEEN_DAMAGE,
         QUEEN_SPEED,
         True,
         False,
         QUEEN_AOE,
         QUEEN_ARROW_DISTANCE)


W = Entity("Witch",
           WITCH_LETTERS,
           WITCH_COLOR,
           WITCH_SIZE,
           WITCH_HEALTH,
           WITCH_DAMAGE,
           WITCH_SPEED,
           True,
           False)
W.alive = False