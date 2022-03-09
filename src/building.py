from .variables import *

class Building:
    all = []
    
    def __init__(self, name: str, color, size, max_health):
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        
        # Initialize
        self.name = name
        self.color = color
        self.size = size
        self.max_health = max_health
        self.health = max_health
        self.alive = True
        
        # Position
        self.X = 0
        self.Y = 0
        
        Building.all.append(self)
        
    def draw(self, posX, posY, sizeX, sizeY): 
        if(2*(posX + sizeX) >= CANVAS_WIDTH):
            return
        if(posY + sizeY >= CANVAS_HEIGHT):
            return
        
        self.X = posX
        self.Y = posY
                
        char = (self.color + "█") if self.alive else " "  
        for y in range(posY, posY + sizeY):
            for x in range(posX*2, posX*2 + sizeX*2):
                CANVAS[y][x] = char
                
    def __repr__(self):
        return f"{self.name}"

# Cannon: Inherits from building
class Cannon(Building):
    all = []
    
    def __init__(self, name: str, color, size, max_health, damage, fire_rate, span):
        # Inherit
        super().__init__(name, color, size, max_health)
        
        # Validate
        assert damage > 0, f"Damage {damage} must be > 0"
        assert fire_rate > 0, f"Fire Rate {fire_rate} must be > 0"
        
        # Initialize
        self.damage = damage
        self.fire_rate = fire_rate
        self.span = span
        
        Cannon.all.append(self)

class Gold_Mine(Building):
    pass

# Instances
th = Building("Townhall", TOWNHALL_COLOR, TOWNHALL_SIZE, TOWNHALL_HEALTH)