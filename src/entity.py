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
        self.clearing_path = False
        self.target_wall = th
        
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
            
        if not self.alive:
            return False
        # if self.clearing_path:
        #     return True
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
            
        def boolean_to_sign(x):
            return int(2*(x - 0.5))
            
        def move_horizontal(sign):
            sign = boolean_to_sign(sign)
            ch = CANVAS[self.Y][self.X + sign*2 + 1]
            if(ch != " " and ch != BARBARIAN_COLOR + "█"):
                if(CANVAS[self.Y][self.X + sign*2 + 1] == Fore.WHITE + "█"):
                    self.clearing_path = True
                    for w in Building.walls:
                        if(self.Y == w.Y and self.X + sign*2 == w.X*2):
                            self.target_wall = w
                            break
                return False
            
            self.clearing_path = False
            self.target_wall = th
            
            clear()
            self.X += sign * 2
            CANVAS[self.Y][self.X] = self.color + "█"
            CANVAS[self.Y][self.X + 1] = self.color + "█"
            return True
            
        def move_vertical(sign):
            sign = boolean_to_sign(sign)
            ch = CANVAS[self.Y + sign][self.X]
            if(ch != " " and ch != BARBARIAN_COLOR + "█"):
                if(CANVAS[self.Y + sign][self.X] == Fore.WHITE + "█"):
                    self.clearing_path = True
                    for w in Building.walls:
                        if(self.Y + sign == w.Y and self.X == w.X*2):
                            self.target_wall = w
                            break
                return False
            
            self.clearing_path = False
            self.target_wall = th
            
            clear()
            self.Y += sign
            CANVAS[self.Y][self.X] = self.color + "█"
            CANVAS[self.Y][self.X + 1] = self.color + "█"
            return True
            
        # flag1 = True if (target.X*2 == self.X) else move_horizontal(target.X*2 > self.X)
        # flag2 = True if (target.Y == self.Y) else move_vertical(target.Y > self.Y)
        flag1 = move_horizontal(target.X*2 > self.X)
        flag2 = move_vertical(target.Y > self.Y)
        
        if(self.clearing_path):
            return True
        
        return not (flag1 and flag2)

    def attack(self, target):
        if(not target.alive):
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
        
        if(CANVAS[self.Y - 1][self.X] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.Y -= 1
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        self.direction = NORTH
        return True
        
    def move_left(self):
        if not self.alive:
            return
        
        if(CANVAS[self.Y][self.X - 2 + 1] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.X -= 2
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        self.direction = WEST
        return True
        
    def move_down(self):
        if not self.alive:
            return
        
        if(CANVAS[self.Y + 1][self.X] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.Y += 1
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        self.direction = SOUTH
        return True
        
    def move_right(self):
        if not self.alive:
            return
        
        if(CANVAS[self.Y][self.X + 2 + 1] != " "):
            return False
        
        def clear():
            CANVAS[self.Y][self.X] = " "
            CANVAS[self.Y][self.X + 1] = " "
        
        clear()
        self.X += 2
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"
        
        self.direction = EAST
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

        if(self.direction == SOUTH):
            ch = CANVAS[self.Y + 1][self.X]
            if(ch != " "):
                for building in Building.all:
                    if not(self.X >= building.X*2 and self.X < (building.X + building.size[0])*2):
                        continue
                    if(self.Y + 1 == building.Y):
                        building.health -= KING_DAMAGE
                        
        if(self.direction == EAST):
            ch = CANVAS[self.Y][self.X + 2]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X + 2 == building.X*2):
                        building.health -= KING_DAMAGE
                        
        if(self.direction == WEST):
            ch = CANVAS[self.Y][self.X - 2]
            if(ch != " "):
                for building in Building.all:
                    if not(self.Y >= building.Y and self.Y < (building.Y + building.size[1])*2):
                        continue
                    if(self.X == building.X*2 + building.size[0]*2):
                        building.health -= KING_DAMAGE
                
    def use_leviathan_axe(self):
        print("King used Leviathan Axe")
    
K = King("Barbarian King",
         KING_COLOR,
         KING_SIZE,
         KING_HEALTH,
         KING_DAMAGE,
         KING_SPEED,
         KING_AXE_DAMAGE,
         KING_AXE_AREA)