from components.gender import Gender, opposite
from config import ENERGY, MAP_HEIGHT, MAP_WIDTH, PLANT_ENERGY
from components.animal import Animal
from components.attributes import Attributes
from components.plant import Plant
from components.point import Point

NEIGHBOUR_TILES = [Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1), Point(-1, 0),
                   Point(-1, 1)]


def filter_capable_to_breed(partners: []):
    return filter(lambda partner: partner.energy > partner.energy_for_breed(), partners)


def get_most_attractive_animal(partners: []):
    most_attractive = partners[0]
    for partner in partners:
        if partner.possibility_of_breeding() > most_attractive.possibility_of_breeding():
            most_attractive = partner
    return [most_attractive]


class Map:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.lower_left = Point(0, 0)
        self.upper_right = Point(self.width, self.height)
        self.animals = []
        self.plants = []
        self.tiles = {}

    def create_random_animal(self, gender):
        position = Point.get_random_point(self.lower_left, self.upper_right)
        while self.tiles.get(position):
            position = Point.get_random_point(self.lower_left, self.upper_right)
        attributes = Attributes.get_random_attributes()

        animal = Animal(gender=gender, position=position, attributes=attributes, age=0, energy=ENERGY['med'])
        self.animals.append(animal)
        self.tiles[position] = animal

    def create_random_plant(self):
        position = Point.get_random_point(self.lower_left, self.upper_right)
        energy = PLANT_ENERGY
        tile = self.tiles.get(position)

        while type(tile) is Animal:
            position = Point.get_random_point(self.lower_left, self.upper_right)
            tile = self.tiles.get(position)
        if type(tile) is Plant:
            energy += tile.energy

        plant = Plant(position=position, energy=energy)
        self.plants.append(plant)

    def check_nearest_tiles_for_food(self, position: Point):
        max_energy = 0
        new_position = position
        for point in NEIGHBOUR_TILES:
            tile = self.tiles.get(position + point)
            if type(tile) is Plant:
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
        if type(plant) is Plant:
            animal.energy += plant.energy
            animal.position = new_position
            self.plants.remove(plant)
            self.tiles[new_position] = animal

    def kill_animal(self, animal: Animal):
        self.animals.remove(animal)
        del self.tiles[animal.position]

    def find_potential_partners(self, position: Point, gender: Gender):
        partners = []
        for point in NEIGHBOUR_TILES:
            tile = self.tiles.get(position + point)
            if type(tile) is Animal and tile.gender is opposite(gender):
                partners.append(tile)
        return partners

    def find_other_animal_to_breed(self, animal: Animal):
        partners = self.find_potential_partners(animal.position, animal.gender)
        partners = filter_capable_to_breed(partners)
        if animal.gender is Gender.F and partners:
            partners = get_most_attractive_animal(partners)
        return partners

    def breed_animals(self, first_animal: Animal, sec_animal: Animal):
        # TODO - implement
        pass

    def find_partners_further(self, animal: Animal):
        # TODO - implement
        pass

    def move_animal(self, animal, new_position):
        # TODO - implement
        pass

    def find_food(self, animal):
        # TODO - implement
        pass
