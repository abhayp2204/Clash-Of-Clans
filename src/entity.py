from .variables import *
from .building import *
from .util import *

class Entity:
    # List of all entities
    all = []
    Barbarians = []
    
    # Class attributes
    damage_rate = 1.0
    health_rate = 1.5
        
    # __init__ is a magic method that gets called whenever an instance is created
    def __init__(self, name: str, color, size, max_health=100, damage=10, speed=1):    
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        assert damage >= 0, f"Damage {damage} must be >= 0"
        assert speed >= 0, f"Damage {damage} must be >= 0"
        
        # Initialize
        self.name = name
        self.color = color
        self.size = size
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.speed = speed
        self.alive = True
        self.target_wall = th
        self.clearing_path = False
        
        self.move_time = 0
        self.attack_time = 0
        self.message = ""
        
        # Add to list of entities
        Entity.all.append(self)
        
        if(name == "Barbarian"):
            Entity.Barbarians.append(self)

    def draw(self, posX, posY): 
        if(2*(posX + self.size[0]) >= CANVAS_WIDTH):
            return
        if(posY + self.size[1] >= CANVAS_HEIGHT):
            return
        
        self.X = posX*2
        self.Y = posY
                
        char = (self.color + "█") if self.alive else " "
        for y in range(posY, posY + self.size[1]):
            for x in range(posX*2, posX*2 + self.size[0]*2):
                CANVAS[y][x] = char

    def move(self, target):
        def erase():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        def redraw():
            CANVAS[self.Y][self.X] = self.color + "█"
            CANVAS[self.Y][self.X + 1] = self.color + "█"
            
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
            self.X -= 2
            redraw()
        def move_right():
            erase()
            self.X += 2
            redraw()
        
            
        if(not self.target_wall.alive):
            self.clearing_path = False
            
        if(target.X*2 > self.X):
            ch = CANVAS[self.Y][self.X + 2]
            if(ch == " " or ch == BARBARIAN_COLOR + "█"):
                move_right()
        elif(target.X*2 < self.X):
            ch = CANVAS[self.Y][self.X - 2]
            if(ch == " " or ch == BARBARIAN_COLOR + "█"):
                move_left()
                
        if(target.Y > self.Y):
            ch = CANVAS[self.Y + 1][self.X]
            if(ch == " " or ch == BARBARIAN_COLOR + "█"):
                move_down()
        elif(target.Y < self.Y):
            ch = CANVAS[self.Y - 1][self.X]
            if(ch == " " or ch == BARBARIAN_COLOR + "█"):
                move_up()
                
        if(target.X*2 > self.X): 
            if(ch == WALL_COLOR + "█"):
                for w in Building.walls:
                    if(self.Y == w.Y and self.X + 2 == w.X*2):
                        self.target_wall = w
                        self.clearing_path = True
                        # w.health = -1
                        return
        elif(target.X*2 < self.X): 
            if(ch == WALL_COLOR + "█"):
                for w in Building.walls:
                    if(self.Y == w.Y and self.X - 2 == w.X*2):
                        self.target_wall = w
                        self.clearing_path = True
                        return
            
        
        if(target.Y > self.Y):
            if(ch == WALL_COLOR + "█"):
                for w in Building.walls:
                    if(self.Y + 1 == w.Y and self.X == w.X*2):
                        self.target_wall = w
                        self.clearing_path = True
                        return
        elif(target.Y < self.Y):
            if(ch == WALL_COLOR + "█"):
                for w in Building.walls:
                    if(self.Y - 1 == w.Y and self.X== w.X*2):
                        self.target_wall = w
                        self.clearing_path = True
                        return
    
    def within_attack_range(self, target):
        dx = int((target.X - self.X/2))
        dy = (target.Y - self.Y)
        
        K.message = "dy =" + str(dy)
        
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
    def __init__(self, name: str, color, size, max_health, damage, speed, axe_damage, axe_area):
        # Inherit
        super().__init__(name, color, size, max_health, damage, speed)
        
        # Validate
        assert axe_damage > 0, f"Damage {axe_damage} must be > 0"
        assert axe_area > 0, f"Fire Rate {axe_area} must be > 0"
        
        # Initialize
        self.health = max_health
        self.axe_damage = axe_damage
        self.axe_area = axe_area
        self.direction = EAST
        
    def move_up(self):
        if not self.alive:
            return
        
        self.direction = NORTH
        if(CANVAS[self.Y - 1][self.X] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.Y -= 1
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        return True
        
    def move_left(self):
        if not self.alive:
            return
        
        self.direction = WEST
        if(CANVAS[self.Y][self.X - 2 + 1] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.X -= 2
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        return True
        
    def move_down(self):
        if not self.alive:
            return
        
        self.direction = SOUTH
        if(CANVAS[self.Y + 1][self.X] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.Y += 1
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        return True
        
    def move_right(self):
        if not self.alive:
            return
        
        self.direction = EAST
        if(CANVAS[self.Y][self.X + 2 + 1] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.X += 2
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        return True
        
    def attack(self):
        if(self.direction == NORTH):
            ch = CANVAS[self.Y - 1][self.X]
            if(ch != " "):
                for building in Building.all:
                    if not(self.X >= building.X*2 and self.X < (building.X + building.size[0])*2):
                        continue
                    if(self.Y == building.Y + building.size[1]):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.X >= w.X*2 and self.X < (w.X + w.size[0])*2):
                        continue
                    if(self.Y == w.Y + w.size[1]):
                        w.health -= KING_DAMAGE

        if(self.direction == SOUTH):
            ch = CANVAS[self.Y + 1][self.X]
            if(ch != " "):
                for building in Building.all:
                    if not(self.X >= building.X*2 and self.X < (building.X + building.size[0])*2):
                        continue
                    if(self.Y + 1 == building.Y):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.X >= w.X*2 and self.X < (w.X + w.size[0])*2):
                        continue
                    if(self.Y + 1 == w.Y):
                        w.health -= KING_DAMAGE
                        
        if(self.direction == EAST):
            ch = CANVAS[self.Y][self.X + 2]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X + 2 == building.X*2):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.Y == w.Y):
                        continue
                    if(self.X + 2 == w.X*2):
                        w.health -= KING_DAMAGE
                        
        if(self.direction == WEST):
            ch = CANVAS[self.Y][self.X - 2]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X == building.X*2 + building.size[0]*2):
                        building.health -= KING_DAMAGE
                for w in Building.walls:
                    if not(self.Y >= w.Y and self.Y < (w.Y + w.size[1])*2):
                        continue
                    if(self.X == w.X*2 + w.size[0]*2):
                        w.health -= KING_DAMAGE
                
    def use_leviathan_axe(self):
        for b in Building.all:
            if(abs(b.X*2 - self.X) <= KING_AXE_AREA and abs(b.Y - self.Y) <= KING_AXE_AREA):
                b.health -= 10000
    
K = King("Barbarian King",
         KING_COLOR,
         KING_SIZE,
         KING_HEALTH,
         KING_DAMAGE,
         KING_SPEED,
         KING_AXE_DAMAGE,
         KING_AXE_AREA)