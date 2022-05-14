from utils import math_utils
from config import COLOR, TAIL, PREFERENCE_FUNCTION, COLOR_THRESHOLD, TAIL_THRESHOLD, GAUSS_SIGMA_COLOR, \
    GAUSS_MU_COLOR, GAUSS_MU_TAIL, GAUSS_SIGMA_TAIL
from utils.preference_function import PreferenceFunction
import scipy.stats


def linear_preference_function(color, tail):
    return (color + tail) / (COLOR['max'] + TAIL['max'])


def threshold_preference_function(color, tail):
    return 1 if color > COLOR_THRESHOLD and tail > TAIL_THRESHOLD else 0


def stabilising_preference_function(color, tail):
    return (scipy.stats.norm(GAUSS_MU_COLOR, GAUSS_SIGMA_COLOR).pdf(color)
            + scipy.stats.norm(GAUSS_MU_TAIL, GAUSS_SIGMA_TAIL).pdf(tail)) / 2


def disruptive_preference_function(color, tail):
    return (scipy.stats.recipinvgauss(GAUSS_MU_COLOR, GAUSS_SIGMA_COLOR).pdf(color)
            + scipy.stats.recipinvgauss(GAUSS_MU_TAIL, GAUSS_SIGMA_TAIL).pdf(tail)) / 2


preference_functions = {
    PreferenceFunction.linear: linear_preference_function,
    PreferenceFunction.threshold: threshold_preference_function,
    PreferenceFunction.stabilising: stabilising_preference_function,
    PreferenceFunction.disruptive: disruptive_preference_function
}


class Attributes:
    color: float
    tail: float

    def __init__(self, color: float, tail: float):
        self.color = color
        self.tail = tail

    def __str__(self):
        return "(" + str(self.color) + "," + str(self.tail) + ")"

    @staticmethod
    def get_random_attributes():
        color = math_utils.get_gauss_in_range(COLOR['min'], COLOR['max'])
        tail = math_utils.get_gauss_in_range(TAIL['min'], TAIL['max'])
        return Attributes(color, tail)

    def probability_of_breeding(self):
        return preference_functions[PREFERENCE_FUNCTION](self.color, self.tail)
