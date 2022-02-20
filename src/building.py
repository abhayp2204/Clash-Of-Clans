from variables import CANNON_DAMAGE, CANNON_FIRE_RATE, CANNON_HEALTH


class Building:
    def __init__(self, name: str, max_health):
        # Validate
        assert max_health > 0, f"Health {max_health} must be > 0"
        
        # Initialize
        self.name = name
        self.max_health = max_health
        
# Townhall inherits from building
class Townhall(Building):
    pass

# Cannon: Inherits from building
class Cannon(Building):
    all = []
    
    def __init__(self, name: str, max_health, damage, fire_rate):
        # Inherit
        super().__init__(name, max_health)
        
        # Validate
        assert damage > 0, f"Damage {damage} must be > 0"
        assert fire_rate > 0, f"Fire Rate {fire_rate} must be > 0"
        
        # Initialize
        self.damage = damage
        self.fire_rate = fire_rate
        
        Cannon.all.append(self)

# Hut inherits from building
class Hut(Building):
    pass
    
townhall = Building("Townhall", 1000)
archer_tower = Building("Archer Tower", 200)

cannon1 = Cannon("Hulk", CANNON_HEALTH, CANNON_DAMAGE, CANNON_FIRE_RATE)
cannon2 = Cannon("Wade", CANNON_HEALTH, CANNON_DAMAGE, CANNON_FIRE_RATE)