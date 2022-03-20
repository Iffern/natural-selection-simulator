from utils import math_utils
from config import COLOR, TAIL


class Attributes:
    def __init__(self, color: float, tail: float):
        self.color = color
        self.tail = tail

    # @staticmethod
    # def get_child_attributes(animal1: Animal, animal2: Animal):
    #     # TODO: add some weights to male and female animal
    #     color = animal1.attributes.color + animal2.attributes.color
    #     tail = animal1.attributes.tail + animal2.attributes.tail
    #     return Attributes(color, tail)

    @staticmethod
    def get_random_attributes():
        color = math_utils.get_gauss_in_range(COLOR['min'], COLOR['max'])
        tail = math_utils.get_gauss_in_range(TAIL['min'], TAIL['max'])
        return Attributes(color, tail)

    def probability_of_breeding(self):
        return (self.color + self.tail)/(COLOR['max'] + TAIL['max'])
