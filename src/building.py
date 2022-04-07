from xml.dom.minidom import Entity
from .variables import *
from . import entity

class Building:
    all = []
    walls = []
    
    def __init__(self, name: str, letters, color, size, max_health):
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        
        # Initialize
        self.name = name
        self.letters = letters
        self.color = color
        self.size = size
        self.max_health = max_health
        self.health = max_health
        self.alive = True
        self.message = ""
        
        # Position
        self.X = 0
        self.Y = 0
        
        if(name == "Wall"):
            Building.walls.append(self)
            return
        Building.all.append(self)
        
    def draw(self, posX, posY): 
        if(X_SCALE*(posX + self.size[0]) >= CANVAS_WIDTH):
            return
        if(posY + self.size[1] >= CANVAS_HEIGHT):
            return
        
        self.X = posX
        self.Y = posY
                
        char = (self.color + BLOCK) if self.alive else " "  
        for y in range(posY, posY + self.size[1]):
            for x in range(posX*2, posX*2 + self.size[0]*2):
                
                # Get letter
                ch = " "
                if y == int((2*posY + self.size[1]) / 2):
                    index = x - posX*2
                    if index < len(self.letters):
                        ch = self.letters[x - posX*2]
                        
                CANVAS[y][x] = self.color + Fore.BLACK + ch + Back.RESET
                if(self.name == "Wall"):
                    CANVAS[y][x] = Fore.WHITE + BLOCK
                    
                perc = 100*(self.health/self.max_health)
                if(perc < 100):
                    CANVAS[y][x] = Back.GREEN + Fore.BLACK + ch + Back.RESET
                if(perc < 50):
                    CANVAS[y][x] = Back.YELLOW + Fore.BLACK + ch + Back.RESET
                if(perc <= 20):
                    CANVAS[y][x] = Back.RED + Fore.BLACK + ch + Back.RESET
                if(perc <= 0):
                    CANVAS[y][x] = " "
                
    def contains_cell(self, X, Y):
        for y in range(self.Y, self.Y + self.size[1]):
            for x in range(self.X, self.X + self.size[0]):
                if(x*2 == X and y == Y):
                    return True
        return False
                
    def __repr__(self):
        return f"{self.name}"

# Cannon: Inherits from Building
class Defender(Building):
    all = []
    
    def __init__(self, name: str, letters, color, size, max_health, damage, fire_rate, aoe, span, land, air):
        # Inherit
        super().__init__(name, letters, color, size, max_health)
        
        # Validate
        assert damage > 0, f"Damage {damage} must be > 0"
        assert fire_rate > 0, f"Fire Rate {fire_rate} must be > 0"
        
        # Initialize
        self.damage = damage
        self.fire_rate = fire_rate
        self.aoe = aoe
        self.span = span
        self.land = land
        self.air = air
        self.fire_time = 0
        self.targets = []
        
        Defender.all.append(self)
        
    def fire(self, target):
        # Make sure that the building can attack the target
        if (self.land and target.land) or (self.air and target.air):
            
            # Only attack target
            if self.aoe == 0:
                if(target.alive):
                    target.health -= self.damage
                th.message = "no aoe"
                
            # Attack all troops near target
            else:
                tgt = []
                half = int(self.aoe / 2)
                for E in entity.Entity.all:
                    x_span = E.X >= target.X - half*X_SCALE and E.X <= target.X + half*X_SCALE
                    y_span = E.Y >= target.Y - half and E.Y <= target.Y + half
                    
                    if x_span and y_span:
                        # tgt.append(E)
                        E.health -= self.damage
                
                    th.message = E.health
                    
            # Overkill
            if(target.health < 0):
                target.health = 0
            
    def in_range(self, troop):
        within_x_span = (troop.X > (self.X - self.size[0] - self.span)*2) and (troop.X < (self.X + self.size[0] + self.span)*2)
        within_y_span = troop.Y > (self.Y - self.size[1] - self.span) and troop.Y < (self.Y + self.size[1] + self.span)
        
        if(within_x_span and within_y_span and not (troop in self.targets)):
            self.targets.append(troop)
            return
        
        if(not(within_x_span and within_y_span) and (troop in self.targets)):
            self.targets.remove(troop)
        
    
class Gold_Mine(Building):
    pass

# Instances
th = Building("Townhall",
               TOWNHALL_LETTERS,
               TOWNHALL_COLOR,
               TOWNHALL_SIZE,
               TOWNHALL_HEALTH)