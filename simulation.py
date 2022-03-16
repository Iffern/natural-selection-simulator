from components.map import Map
from components.point import Point

world_map = Map()
world_map.create_random_animal()
world_map.create_random_plant()

plant = world_map.plants[0]
animal = world_map.animals[0]
print(plant.position, plant.energy)
print(animal.position, animal.energy, animal.attributes.color, animal.attributes.tail, animal.gender, animal.age)

animal.move(Point(3, 4))
print(animal.position)

