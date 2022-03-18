import math
import random


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

    def get_child_position(self):
        child_x = 0
        child_y = 0
        diff = [-1, 0, 1]

        while not (abs(child_x) or abs(child_y)):
            child_x = random.choice(diff)
            child_y = random.choice(diff)

        return self + Point(child_x, child_y)

    @staticmethod
    def get_random_point(point_lower_left, point_upper_right):
        x = random.randint(point_lower_left.x, point_upper_right.x)
        y = random.randint(point_lower_left.y, point_upper_right.y)
        return Point(x, y)
