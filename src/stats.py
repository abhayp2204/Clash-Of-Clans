from entity import *
from building import *

def building_stats():
    print(f"{townhall.name} health = {townhall.health}")
    print(f"{archerTower.name} health = {archerTower.health}")
    
def entity_stats():
    for entity in Entity.all:
        print(f"*** {entity.name} ***")
        print(f"Health = {entity.health}")
        print(f"Damage = {entity.damage}")
        print(f"Speed = {entity.speed}")
        print()