from components.animal import Animal
from utils import math_utils
from config import COLOR, TAIL


class Attributes:
    def __init__(self, color: float, tail: float):
        self.color = color
        self.tail = tail

    @staticmethod
    def get_child_attributes(male: Animal, female: Animal):
        color = 0.5*male.attributes.color + 0.5*female.attributes.color
        tail = 0.5*male.attributes.tail + 0.5*female.attributes.tail
        return Attributes(color, tail)

    @staticmethod
    def get_random_attributes():
        color = math_utils.get_gauss_in_range(COLOR['min'], COLOR['max'])
        tail = math_utils.get_gauss_in_range(TAIL['min'], TAIL['max'])
        return Attributes(color, tail)

    def probability_of_breeding(self):
        return (self.color + self.tail) / (COLOR['max'] + TAIL['max'])
