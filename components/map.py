from config import ENERGY, MAP_HEIGHT, MAP_WIDTH, PLANT_ENERGY
from components.animal import Animal
from components.attributes import Attributes
from components.gender import Gender
from components.plant import Plant
from components.point import Point


class Map:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.lower_left = Point(0, 0)
        self.upper_right = Point(self.width, self.height)
        self.animals = []
        self.plants = []

    def create_random_animal(self):
        gender = Gender.random()
        position = Point.get_random_point(self.lower_left, self.upper_right)
        attributes = Attributes.get_random_attributes()

        animal = Animal(gender=gender, position=position, attributes=attributes, age=0, energy=ENERGY['max'])
        self.animals.append(animal)

    def create_random_plant(self):
        position = Point.get_random_point(self.lower_left, self.upper_right)
        plant = Plant(position=position, energy=PLANT_ENERGY)
        self.plants.append(plant)


