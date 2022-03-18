from enum import Enum
import random


class Gender(Enum):
    F = "Female"
    M = "Male"

    @staticmethod
    def random():
        return random.choice(list(Gender))
