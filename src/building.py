from .variables import *

class Building:
    all = []
    walls = []
    
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
        self.message = ""
        
        # Position
        self.X = 0
        self.Y = 0
        
        if(name == "Wall"):
            Building.walls.append(self)
            return
        Building.all.append(self)
        
    def draw(self, posX, posY): 
        if(2*(posX + self.size[0]) >= CANVAS_WIDTH):
            return
        if(posY + self.size[1] >= CANVAS_HEIGHT):
            return
        
        self.X = posX
        self.Y = posY
                
        char = (self.color + "█") if self.alive else " "  
        for y in range(posY, posY + self.size[1]):
            for x in range(posX*2, posX*2 + self.size[0]*2):
                CANVAS[y][x] = self.color + "█"
                if(self.name == "Wall"):
                    CANVAS[y][x] = Fore.WHITE + "█"
                    
                perc = 100*(self.health/self.max_health)
                if(perc < 100):
                    CANVAS[y][x] = Fore.GREEN + "█"
                if(perc < 50):
                    CANVAS[y][x] = Fore.YELLOW + "█"
                if(perc <= 20):
                    CANVAS[y][x] = Fore.RED + "█"
                if(perc <= 0):
                    CANVAS[y][x] = " "
                
    def __repr__(self):
        return f"{self.name}"

# Cannon: Inherits from Building
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
        self.fire_time = 0
        self.targets = []
        
        Cannon.all.append(self)
        
    def fire(self, target):
        if(target.alive):
            target.health -= self.damage
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
               TOWNHALL_COLOR,
               TOWNHALL_SIZE,
               TOWNHALL_HEALTH)