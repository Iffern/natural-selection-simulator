import random

from components.attributes import Attributes
from components.gender import Gender
from components.point import Point, NEIGHBOUR_TILES
from config import ENERGY_DEMAND_PER_ROUND, BREED_ENERGY_FEMALE, BREED_ENERGY_MALE
from utils.crossover import Crossover
import pygame


class Animal:
    gender: Gender
    position: Point
    attributes: Attributes
    age: int
    energy: float

    def __init__(self, gender: Gender, position: Point, attributes: Attributes, age: int, energy: float):
        self.gender = gender
        self.position = position
        self.attributes = attributes
        self.age = age
        self.energy = energy

    def move(self, vector: Point):
        self.position += vector

    def can_breed(self, f_breed_energy=BREED_ENERGY_FEMALE, m_breed_energy=BREED_ENERGY_MALE):
        if self.gender == Gender.F:
            return self.energy >= f_breed_energy
        else:
            return self.energy >= m_breed_energy

    def eat(self, energy_demand_per_round=ENERGY_DEMAND_PER_ROUND):
        if self.energy - energy_demand_per_round >= 0:
            self.energy -= energy_demand_per_round
            return True
        else:
            return False

    def energy_for_breed(self, f_breed_energy=BREED_ENERGY_FEMALE, m_breed_energy=BREED_ENERGY_MALE):
        return f_breed_energy if self.gender is Gender.F else m_breed_energy

    def probability_of_breeding(self):
        return self.attributes.probability_of_breeding()

    def create_child(self, partner, tiles: {}, crossover: Crossover, is_in_bounds,
                     energy_demand_per_round=ENERGY_DEMAND_PER_ROUND):
        return Animal(gender=Gender.random(), position=Animal.get_child_position(self.position, tiles, is_in_bounds),
                      attributes=crossover.get_crossover(self.attributes, partner.attributes), age=0,
                      energy=4 * energy_demand_per_round)

    def get_image(self):
        return 'gui/resources/peacock_female.png' if self.gender == Gender.F else 'gui/resources/peacock_male.png'

    def display(self, screen, scale: Point):
        display_size = 50
        display_position = (scale.x * self.position.x + scale.x/2 - display_size/2,
                            scale.y * self.position.y + scale.y/2 - display_size/2)
        scaled_image = pygame.transform.scale(pygame.image.load(self.get_image()), (display_size, display_size))
        screen.blit(scaled_image, display_position)

    @staticmethod
    def get_child_position(point: Point, tiles: {}, is_in_bounds):
        possible_places = NEIGHBOUR_TILES.copy()
        place = random.choice(possible_places)
        while (isinstance(tiles.get(point + place), Animal) or not is_in_bounds(point + place)) and possible_places:
            possible_places.remove(place)
            if possible_places:
                place = random.choice(possible_places)
            else:
                return point
        return point + place
