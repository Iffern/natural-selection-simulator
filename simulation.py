from statistics import mean
from components.gender import Gender
from components.map import Map
import pygame
from pygame.rect import Rect
from gui import gui_config


def get_average_color(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    color_values = list(map(lambda ani: ani.attributes.color, males))
    return mean(color_values)


def get_average_tail(animals: []):
    males = list(filter(lambda ani: ani.gender is Gender.M, animals))
    tail_values = list(map(lambda ani: ani.attributes.tail, males))
    return mean(tail_values)


def get_number_of_animals(animals: [], gender: Gender):
    return len(list(filter(lambda ani: ani.gender is gender, animals)))


pygame.init()

screen = pygame.display.set_mode([gui_config.WIDTH, gui_config.HEIGHT])
pygame.display.set_caption("Natural selection simulator")

screen.fill((255, 255, 255))
world_map = Map(screen=screen)

open('results.txt', 'w').close()

epoch = 0
interval = 2000
next_tick = interval

while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    pygame.draw.rect(screen, (188, 235, 134), Rect(0, 0, gui_config.WIDTH - gui_config.BAR_WIDTH, gui_config.HEIGHT))

    tick = pygame.time.get_ticks()
    if tick > next_tick:
        next_tick += interval

        world_map.create_plants_per_round()
        world_map.animals_sim_step()

        with open("results.txt", "a") as results:
            results.write(str(get_average_color(world_map.animals)) + ";" + str(get_average_tail(world_map.animals)) + ";"
                          + str(get_number_of_animals(world_map.animals, Gender.F)) + ";"
                          + str(get_number_of_animals(world_map.animals, Gender.M)) + ";" + str(epoch) + "\n")
        epoch += 1

    world_map.display(events)
    pygame.display.flip()
