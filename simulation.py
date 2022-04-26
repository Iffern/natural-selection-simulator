import time
from statistics import mean

from components.gender import Gender
from components.map import Map

import pygame
import pygame_widgets
from pygame.rect import Rect


from config import NUMBER_OF_MALE_ANIMALS, NUMBER_OF_FEMALE_ANIMALS, PLANT_GROWTH_PER_ROUND
from gui import gui_config
from gui.sidebar import SideBar


def get_average_color(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    color_values = list(map(lambda ani: ani.attributes.color, males))
    return mean(color_values)


def get_average_tail(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    tail_values = list(map(lambda ani: ani.attributes.tail, males))
    return mean(tail_values)


pygame.init()

screen = pygame.display.set_mode([gui_config.WIDTH, gui_config.HEIGHT])
pygame.display.set_caption("Natural selection simulator")

side_bar = SideBar(gui_config.WIDTH - gui_config.BAR_WIDTH, 50)

screen.fill((255, 255, 255))

# TODO: move to some menu component and get parameters from sliders
side_bar.add_slider(screen, 0, "Number of males", 1, 20, 4)
side_bar.add_slider(screen, 70, "Number of females", 1, 20, 4)
side_bar.add_slider(screen, 140, "Plant growth per round", 1, 100, 10)
side_bar.add_slider(screen, 210, "Plant energy value", 1, 100, 5)
side_bar.add_slider(screen, 280, "Animal energy demand per day", 1, 20, 3)
side_bar.add_slider(screen, 350, "Breeding energy demand - female", 1, 90, 15)
side_bar.add_slider(screen, 420, "Breeding energy demand - male", 1, 90, 15)
side_bar.add_slider(screen, 490, "Maximum animal age - in rounds", 1, 300, 100)

world_map = Map(screen=screen)

for i in range(NUMBER_OF_MALE_ANIMALS):
    world_map.create_random_animal(Gender.M)

for i in range(NUMBER_OF_FEMALE_ANIMALS):
    world_map.create_random_animal(Gender.F)


def get_number_of_animals(animals: [], gender: Gender):
    return len(list(filter(lambda ani: ani.gender is gender, animals)))


open('results.txt', 'w').close()

epoch = 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    pygame.draw.rect(screen, (188, 235, 134), Rect(0, 0, gui_config.WIDTH - gui_config.BAR_WIDTH, gui_config.HEIGHT))
    side_bar.update_sliders()
    pygame_widgets.update(events)

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
    with open("results.txt", "a") as results:
        results.write(str(get_average_color(world_map.animals)) + ";" + str(get_average_tail(world_map.animals)) + ";"
                      + str(get_number_of_animals(world_map.animals, Gender.F)) + ";"
                      + str(get_number_of_animals(world_map.animals, Gender.M)) + ";" + str(epoch) + "\n")
    epoch += 1

    world_map.display()

    # TODO: change to pygame clock
    time.sleep(2)
    pygame.display.flip()
