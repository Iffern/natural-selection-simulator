from components.attributes import Attributes
from components.gender import Gender
from components.point import Point


class Animal:

    def __init__(self, gender: Gender, position: Point, attributes: Attributes, age: int, energy: float):
        self.gender = gender
        self.position = position
        self.attributes = attributes
        self.age = age
        self.energy = energy

    def move(self, vector: Point):
        self.position += vector

    def create_child(self, partner):
        # TODO
        # return Animal(gender=Gender.random(), position=Point.get_child_position(self.position),
        #               attributes=Attributes.get_child_attributes(self, partner), age=0, energy=100.0)
        pass
