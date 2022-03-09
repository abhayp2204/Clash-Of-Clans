from .variables import *

class Building:
    all = []
    
    def __init__(self, name: str, color, max_health):
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        
        # Initialize
        self.name = name
        self.color = color
        self.max_health = max_health
        self.health = max_health
        
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
                
        for y in range(posY, posY + sizeY):
            for x in range(posX*2, posX*2 + sizeX*2):
                CANVAS[y][x] = self.color + "█"

# Cannon: Inherits from building
class Cannon(Building):
    all = []
    
    def __init__(self, name: str, color, max_health, damage, fire_rate, span):
        # Inherit
        super().__init__(name, color, max_health)
        
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