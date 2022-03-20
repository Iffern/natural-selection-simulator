from components.point import Point

MAP_WIDTH = 100
MAP_HEIGHT = 100

COLOR = {'min': 0, 'max': 100}
TAIL = {'min': 0, 'max': 100}
ENERGY = {'min': 0, 'med': 50, 'max': 100}

PLANT_ENERGY = 5
ENERGY_DEMAND_PER_ROUND = 3
BREED_ENERGY_FEMALE = 15
BREED_ENERGY_MALE = 7

NUMBER_OF_MALE_ANIMALS = 5
NUMBER_OF_FEMALE_ANIMALS = 5

PLANT_GROWTH_PER_ROUND = 5
NEIGHBOUR_TILES = [Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1), Point(-1, 0),
                   Point(-1, 1)]