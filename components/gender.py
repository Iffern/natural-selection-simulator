from enum import Enum
import random


class Gender(Enum):
    F = "Female"
    M = "Male"

    @staticmethod
    def random():
        return random.choice(list(Gender))


def opposite(gender: Gender):
    return Gender.M if gender == Gender.F else Gender.F
