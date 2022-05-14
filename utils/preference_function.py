from enum import Enum


class PreferenceFunction(Enum):
    threshold = 1,
    linear = 2,
    stabilising = 3,
    disruptive = 4,
