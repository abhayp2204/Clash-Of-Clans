from variables import *

class Entity:
    # List of all entities
    all = []
    
    # Class attributes
    damage_rate = 1.0
    health_rate = 1.5
        
    # __init__ is a magic method that gets called whenever an instance is created
    def __init__(self, name: str, max_health=100, damage=10, speed=1):    
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        assert damage >= 0, f"Damage {damage} must be >= 0"
        assert speed >= 0, f"Damage {damage} must be >= 0"
        
        # Initialize
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.speed = speed
        
        # Add to list of entities
        Entity.all.append(self)

    def attack(self):
        print(f"Entity attacks with damage {self.damage}")
        
    def apply_rage_spell(self):
        self.damage *= 2
        self.speed *= 2
        
    def apply_heal_spell(self):
        self.health *= 1.5
        if(self.health > self.max_health):
            self.health = self.max_health

    # Customized representation of the object
    def __repr__(self):
        return f"{self.name}"
        
# Instances
King = Entity("King", KING_HEALTH, KING_DAMAGE, KING_SPEED)

Barbarian = []
for i in range(20):
    Barbarian.append(Entity("Barbarian", BARBARIAN_HEALTH, BARBARIAN_DAMAGE, BARBARIAN_SPEED))
    