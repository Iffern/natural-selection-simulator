import math
import random

from components.animal import Animal
from config import NEIGHBOUR_TILES


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __eq__(self, point):
        return self.x == self.y and point.x == point.y

    def __ne__(self, point):
        return not self == point

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def get_child_position(self, tiles: []):
        possible_places = NEIGHBOUR_TILES.copy()
        place = random.choice(possible_places)
        while type(tiles.get(self + place)) is Animal and possible_places:
            possible_places.remove(place)
            place = random.choice(possible_places)
        return self + place if possible_places else self

    @staticmethod
    def get_random_point(point_lower_left, point_upper_right):
        x = random.randint(point_lower_left.x, point_upper_right.x)
        y = random.randint(point_lower_left.y, point_upper_right.y)
        return Point(x, y)
