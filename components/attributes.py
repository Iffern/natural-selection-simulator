import random


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
        color = round(random.uniform(0, 100), 2)
        tail = round(random.uniform(0, 100), 2)
        return Attributes(color, tail)


