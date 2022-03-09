from .entity import *
from .building import *

def building_stats():
    for building in Building.all:
        print(f"*** {building.name} ***")
        print(f"Health: {building.max_health}")
        # print(f"Damage: {cannon.damage}")
        print()
        
def entity_stats():
    for entity in Entity.all:
        print(f"*** {entity.name} ***")
        print(f"Health = {entity.health}")
        print(f"Damage = {entity.damage}")
        print(f"Speed = {entity.speed}")
        print()