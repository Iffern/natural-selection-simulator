import time
from statistics import mean

from components.gender import Gender
from components.map import Map

from config import NUMBER_OF_MALE_ANIMALS, NUMBER_OF_FEMALE_ANIMALS, PLANT_GROWTH_PER_ROUND

world_map = Map()

for i in range(NUMBER_OF_MALE_ANIMALS):
    world_map.create_random_animal(Gender.M)

for i in range(NUMBER_OF_FEMALE_ANIMALS):
    world_map.create_random_animal(Gender.F)


def get_average_color(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    color_values = list(map(lambda ani: ani.attributes.color, males))
    return mean(color_values)


def get_average_tail(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    tail_values = list(map(lambda ani: ani.attributes.tail, males))
    return mean(tail_values)


while True:
    for i in range(PLANT_GROWTH_PER_ROUND):
        world_map.create_random_plant()
    for animal in world_map.animals:
        can_animal_eat = animal.eat()
        if not can_animal_eat:
            world_map.find_food_or_die(animal)
        else:
            if animal.can_breed():
                partners = world_map.find_other_animal_to_breed(animal)
                if partners:
                    for partner in partners:
                        world_map.breed_animals(animal, partner)
                else:
                    new_position = world_map.find_partners_further(animal)
                    if new_position and new_position != animal.position:
                        world_map.move_animal(animal, new_position)
                    else:
                        world_map.find_food(animal)
            else:
                world_map.find_food(animal)
    print(*list(map(lambda ani: ani.position, world_map.animals)))
    print("Average color: " + str(get_average_color(world_map.animals)))
    print("Average tail: " + str(get_average_tail(world_map.animals)))
    time.sleep(2)
