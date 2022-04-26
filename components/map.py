from random import random

from components.gender import Gender, opposite
from config import ENERGY, MAP_HEIGHT, MAP_WIDTH, PLANT_ENERGY
from gui.gui_config import WIDTH, HEIGHT, BAR_WIDTH
from components.animal import Animal
from components.attributes import Attributes
from components.plant import Plant
from components.point import Point, NEIGHBOUR_TILES
from utils.crossover import Crossover, BlendCrossoverAB


def filter_capable_to_breed(partners: []):
    return list(filter(lambda partner: partner.energy > partner.energy_for_breed(), partners))


def get_most_attractive_animal(partners: []):
    most_attractive = partners[0]
    for partner in partners:
        if partner.attributes.probability_of_breeding() > most_attractive.attributes.probability_of_breeding():
            most_attractive = partner
    return [most_attractive]


class Map:
    width: int
    height: int
    lower_left: Point
    upper_right: Point
    animals: list
    plants: list
    tiles: dict
    crossover: Crossover
    scale: Point

    def __init__(self, width: int = None, height: int = None, screen=None):
        self.width = width or MAP_WIDTH
        self.height = height or MAP_HEIGHT
        self.lower_left = Point(0, 0)
        self.upper_right = Point(self.width - 1, self.height - 1)
        self.animals = []
        self.plants = []
        self.tiles = {}
        self.crossover = BlendCrossoverAB()     # TODO: add to config
        self.screen = screen
        self.scale = Point((WIDTH - BAR_WIDTH)/MAP_WIDTH, HEIGHT/MAP_HEIGHT)

    def is_position_in_bounds(self, position: Point):
        return self.lower_left <= position <= self.upper_right

    def create_random_animal(self, gender):
        position = Point.get_random_point(self.lower_left, self.upper_right)
        while self.tiles.get(position):
            position = Point.get_random_point(self.lower_left, self.upper_right)
        attributes = Attributes.get_random_attributes()

        animal = Animal(gender=gender, position=position, attributes=attributes, age=0, energy=ENERGY['max'])
        self.animals.append(animal)
        self.tiles[position] = animal

    def create_random_plant(self):
        position = Point.get_random_point(self.lower_left, self.upper_right)
        energy = PLANT_ENERGY
        tile = self.tiles.get(position)

        while isinstance(tile, Animal):
            position = Point.get_random_point(self.lower_left, self.upper_right)
            tile = self.tiles.get(position)
        if isinstance(tile, Plant):
            energy += tile.energy

        plant = Plant(position=position, energy=energy)
        self.plants.append(plant)
        self.tiles[position] = plant

    def check_nearest_tiles_for_food(self, position: Point):
        max_energy = 0
        new_position = position
        for point in NEIGHBOUR_TILES:
            tile = self.tiles.get(position + point)
            if isinstance(tile, Plant) and tile.energy > max_energy:
                max_energy = max(tile.energy, max_energy)
                new_position = position + point
        return new_position

    def find_food_or_die(self, animal: Animal):
        animal_position = animal.position
        new_position = self.check_nearest_tiles_for_food(animal_position)
        if animal_position != new_position:
            self.animal_eats_plant(animal, new_position)
            if animal.eat():
                return
        self.kill_animal(animal)

    def animal_eats_plant(self, animal: Animal, new_position: Point):
        plant = self.tiles.get(new_position)
        if isinstance(plant, Plant):
            animal.energy += plant.energy
            self.plants.remove(plant)
            self.move_animal(animal, new_position)

    def kill_animal(self, animal: Animal):
        self.animals.remove(animal)
        del self.tiles[animal.position]

    def find_potential_partners(self, position: Point, gender: Gender):
        partners = []
        for point in NEIGHBOUR_TILES:
            tile = self.tiles.get(position + point)
            if isinstance(tile, Animal) and tile.gender is opposite(gender):
                partners.append(tile)
        return partners

    def find_other_animal_to_breed(self, animal: Animal):
        partners = self.find_potential_partners(animal.position, animal.gender)
        partners = filter_capable_to_breed(partners)
        if animal.gender is Gender.F and partners:
            partners = get_most_attractive_animal(partners)
        return partners

    def breed_animals(self, first_animal: Animal, sec_animal: Animal):
        female = first_animal if first_animal.gender is Gender.F else sec_animal
        male = first_animal if first_animal.gender is Gender.M else sec_animal
        random_num = random()
        if random_num <= male.probability_of_breeding():
            child = female.create_child(male, self.tiles, self.crossover, self.is_position_in_bounds)
            # if there is no free position around female, we don't create a child
            if child.position is not female.position:
                self.tiles[child.position] = child
                self.animals.append(child)

    def find_partners_further(self, animal: Animal):
        position = animal.position
        position_partners_map = {}
        for point in NEIGHBOUR_TILES:
            new_position = position + point
            if not isinstance(self.tiles.get(new_position), Animal):
                partners = self.find_potential_partners(new_position, animal.gender)
                position_partners_map[new_position] = partners
        if animal.gender is Gender.F and position_partners_map:
            return self.get_position_next_to_most_attractive_partner(position_partners_map)
        elif animal.gender is Gender.M and position_partners_map:
            return self.get_position_with_largest_number_of_females(position_partners_map)
        return position

    def get_position_next_to_most_attractive_partner(self, position_partners_map: {}):
        result_position = None
        most_attractive = None
        for position, partners in position_partners_map.items():
            for partner in partners:
                if (most_attractive is None or partner.attributes.probability_of_breeding() >
                    most_attractive.attributes.probability_of_breeding()) \
                        and self.is_position_in_bounds(position):
                    most_attractive = partner
                    result_position = position
        return result_position

    def get_position_with_largest_number_of_females(self, position_partners_map):
        result_position = None
        max_females = 0
        for position, partners in position_partners_map.items():
            females_around_position = len(partners)
            if females_around_position > max_females and self.is_position_in_bounds(position):
                result_position = position
                max_females = females_around_position
        return result_position

    def move_animal(self, animal: Animal, new_position: Point or None):
        if new_position and self.is_position_in_bounds(new_position):
            del self.tiles[animal.position]
            animal.position = new_position
            self.tiles[new_position] = animal

    def find_food(self, animal: Animal):
        new_position, energy = self.find_tile_with_largest_amount_of_food(animal.position)
        if new_position:
            animal.energy += energy
            self.move_animal(animal, new_position)
        else:
            new_position = self.find_food_further(animal.position)
            self.move_animal(animal, new_position)

    def find_tile_with_largest_amount_of_food(self, position: Point):
        new_position = None
        max_energy = 0
        for point in NEIGHBOUR_TILES:
            plant_position = position + point
            plant = self.tiles.get(plant_position)
            if isinstance(plant, Plant) and plant.energy > max_energy:
                max_energy = plant.energy
                new_position = plant_position
        return new_position, max_energy

    def find_food_further(self, position: Point):
        result_position = position
        max_energy = 0
        for point in NEIGHBOUR_TILES:
            new_position = position + point
            if not isinstance(self.tiles.get(new_position), Animal):
                position_with_food, energy = self.find_tile_with_largest_amount_of_food(new_position)
                if energy > max_energy:
                    max_energy = energy
                    result_position = new_position
        if result_position is position:
            result_position = self.get_free_neighbour_position(position)
        return result_position

    def get_free_neighbour_position(self, position):
        for point in NEIGHBOUR_TILES:
            new_position = position + point
            if not isinstance(self.tiles.get(new_position), Animal) and self.is_position_in_bounds(new_position):
                return new_position
        return position

    def display(self):
        for a in self.animals:
            a.display(self.screen, self.scale)

        for p in self.plants:
            p.display(self.screen, self.scale)
