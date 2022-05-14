from utils.preference_function import PreferenceFunction

MAP_WIDTH = 10
MAP_HEIGHT = 10

COLOR = {'min': 0, 'max': 100}
TAIL = {'min': 0, 'max': 100}
ENERGY = {'min': 0, 'med': 50, 'max': 100}

PLANT_ENERGY = 5
ENERGY_DEMAND_PER_ROUND = 3
BREED_ENERGY_FEMALE = 15
BREED_ENERGY_MALE = 7

NUMBER_OF_MALE_ANIMALS = 5
NUMBER_OF_FEMALE_ANIMALS = 10

PLANT_GROWTH_PER_ROUND = 1

PREFERENCE_FUNCTION = PreferenceFunction.linear

COLOR_THRESHOLD = 0.5
TAIL_THRESHOLD = 0.5

GAUSS_MU_COLOR = 0.5
GAUSS_SIGMA_COLOR = 0.1
GAUSS_MU_TAIL = 0.5
GAUSS_SIGMA_TAIL = 0.1


CROSSOVER = {'blx': {'alpha': 0.125, 'beta': 0.125}, 'w_avg': {'alpha': 0.2, 'beta': 0.8}}
