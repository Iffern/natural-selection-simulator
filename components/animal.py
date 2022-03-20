from components.attributes import Attributes
from components.gender import Gender
from components.point import Point
from config import ENERGY_DEMAND_PER_ROUND, BREED_ENERGY_FEMALE, BREED_ENERGY_MALE


class Animal:

    def __init__(self, gender: Gender, position: Point, attributes: Attributes, age: int, energy: float):
        self.gender = gender
        self.position = position
        self.attributes = attributes
        self.age = age
        self.energy = energy

    def move(self, vector: Point):
        self.position += vector

    def can_breed(self):
        if self.gender == Gender.F:
            return self.energy >= BREED_ENERGY_FEMALE
        else:
            return self.energy >= BREED_ENERGY_MALE

    def eat(self):
        if self.energy - ENERGY_DEMAND_PER_ROUND >= 0:
            self.energy -= ENERGY_DEMAND_PER_ROUND
            return True
        else:
            return False

    def energy_for_breed(self):
        return BREED_ENERGY_FEMALE if self.gender is Gender.F else BREED_ENERGY_MALE

    def probability_of_breeding(self):
        return self.attributes.probability_of_breeding()

    def create_child(self, partner):
        # TODO
        # return Animal(gender=Gender.random(), position=Point.get_child_position(self.position),
        #               attributes=Attributes.get_child_attributes(self, partner), age=0, energy=100.0)
        pass
