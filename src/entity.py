from re import X
from .variables import *

class Entity:
    # List of all entities
    all = []
    
    # Class attributes
    damage_rate = 1.0
    health_rate = 1.5
        
    # __init__ is a magic method that gets called whenever an instance is created
    def __init__(self, name: str, color, max_health=100, damage=10, speed=1):    
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        assert damage >= 0, f"Damage {damage} must be >= 0"
        assert speed >= 0, f"Damage {damage} must be >= 0"
        
        # Initialize
        self.name = name
        self.color = color
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.speed = speed
        
        # Position
        self.X = 1
        self.Y = 2
        
        # Add to list of entities
        Entity.all.append(self)

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

    def move(self):
        CANVAS[self.Y][self.X] = " "
        CANVAS[self.Y][self.X + 1] = " "
        self.X += 2
        CANVAS[self.Y][self.X] = self.color + "█"
        CANVAS[self.Y][self.X + 1] = self.color + "█"

    def attack(self):
        print(f"Entity attacks with damage {self.damage}")
        
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
    def __init__(self, name: str, color, max_health, damage, speed, axe_damage, axe_area):
        # Inherit
        super().__init__(name, color, max_health, damage, speed)
        
        # Validate
        assert axe_damage > 0, f"Damage {axe_damage} must be > 0"
        assert axe_area > 0, f"Fire Rate {axe_area} must be > 0"
        
        # Initialize
        self.axe_damage = axe_damage
        self.axe_area = axe_area
        
    def use_leviathan_axe(self):
        print("King used Leviathan Axe")
    