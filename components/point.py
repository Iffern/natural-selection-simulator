import math
import random


class Point:
    x: int
    y: int

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

    def __hash__(self):
        return 17*hash(self.x) + 19*hash(self.y)

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    @staticmethod
    def get_random_point(point_lower_left, point_upper_right):
        x = random.randint(point_lower_left.x, point_upper_right.x)
        y = random.randint(point_lower_left.y, point_upper_right.y)
        return Point(x, y)


NEIGHBOUR_TILES = [Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1), Point(-1, 0),
                   Point(-1, 1)]
