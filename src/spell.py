from .variables import *
from .entity import Entity

class Spell:
    # __init__ is a magic method that gets called whenever an instance is created
    def __init__(self, number, duration, health_boost, damage_boost, speed_boost):
        # Validate
        
        # Initialize
        self.number = number
        
        self.health_boost = health_boost
        self.damage_boost = damage_boost
        self.speed_boost = speed_boost
        
        self.time = 0
        self.duration = duration
        self.active = False
        
    def apply(self, timesteps):
        self.time = timesteps
        self.active = True
        
        for E in Entity.all:
            E.health *= self.health_boost
            if(E.health > E.max_health):
                E.health = E.max_health
                
            E.damage *= self.damage_boost
            E.speed *= self.speed_boost
            
    def reset(self):
        self.active = False
        for troop in Entity.all:
            troop.damage = BARBARIAN_DAMAGE
            troop.speed = BARBARIAN_SPEED
            
Rage = Spell(NUM_RAGE_SPELLS, RAGE_DURATION, RAGE_HEALTH_BUFF, RAGE_DAMAGE_BUFF, RAGE_SPEED_BUFF)
Heal = Spell(NUM_HEAL_SPELLS, 1, 1.5, 1, 1)