import unittest

from components.animal import Animal
from components.attributes import Attributes
from components.gender import Gender
from components.map import filter_capable_to_breed, get_most_attractive_animal, Map
from components.plant import Plant
from components.point import Point
from config import BREED_ENERGY_MALE, MAP_WIDTH, MAP_HEIGHT, ENERGY, PLANT_ENERGY, ENERGY_DEMAND_PER_ROUND, \
    BREED_ENERGY_FEMALE


def _get_animal_with_energy(energy: float):
    return Animal(Gender.M, Point(0, 0), Attributes(0.5, 0.5), 1, energy)


def _get_animal_with_attributes(attributes: Attributes):
    return Animal(Gender.M, Point(0, 0), attributes, 1, BREED_ENERGY_MALE)


def _get_animal_on_position(position: Point):
    return Animal(Gender.F, position, Attributes(0.5, 0.5), 1, 0)


def _get_animal_on_position_with_gender(position: Point, gender: Gender):
    return Animal(gender, position, Attributes(0.5, 0.5), 1, 0)


def _get_animal_on_position_with_energy(position: Point, energy: float):
    return Animal(Gender.F, position, Attributes(0.5, 0.5), 1, energy)


class MapTest(unittest.TestCase):

    def test_filter_capable_to_breed(self):
        animal1 = _get_animal_with_energy(BREED_ENERGY_MALE + 1)
        animal2 = _get_animal_with_energy(BREED_ENERGY_MALE - 1)
        animal3 = _get_animal_with_energy(BREED_ENERGY_MALE)
        partners = [animal1, animal2, animal3]
        result = filter_capable_to_breed(partners)
        self.assertGreaterEqual(result, [animal1])

    def test_get_most_attractive_animal(self):
        animal1 = _get_animal_with_attributes(Attributes(0.2, 0.2))
        animal2 = _get_animal_with_attributes(Attributes(0.7, 0.4))
        animal3 = _get_animal_with_attributes(Attributes(0.4, 0.7))
        partners = [animal1, animal2, animal3]
        result = get_most_attractive_animal(partners)
        self.assertEqual(result, [animal2])

    def test_is_position_in_bounds(self):
        world = Map()
        self.assertTrue(world.is_position_in_bounds(Point(0, 0)))
        self.assertTrue(world.is_position_in_bounds(Point(MAP_WIDTH - 1, MAP_HEIGHT - 1)))
        self.assertFalse(world.is_position_in_bounds(Point(-1, 0)))
        self.assertFalse(world.is_position_in_bounds(Point(MAP_WIDTH - 1, MAP_HEIGHT)))
        self.assertFalse(world.is_position_in_bounds(Point(MAP_WIDTH, 0)))
        self.assertFalse(world.is_position_in_bounds(Point(0, MAP_HEIGHT)))

    def test_create_random_animal(self):
        world = Map()
        world.create_random_animal(Gender.M)
        self.assertEqual(len(world.animals), 1)
        self.assertEqual(len(world.tiles), 1)
        animal = world.animals[0]
        position = animal.position
        self.assertEqual(world.tiles[position], animal)
        self.assertEqual(animal.gender, Gender.M)
        self.assertEqual(animal.age, 0)
        self.assertEqual(animal.energy, ENERGY['max'])

    def test_create_random_plant(self):
        world = Map(width=2, height=2)
        world.create_random_plant()
        self.assertEqual(len(world.plants), 1)
        self.assertEqual(len(world.tiles), 1)

        world = Map(width=2, height=2)
        world.tiles = {Point(0, 0): (_get_animal_on_position(Point(0, 0))),
                       Point(1, 0): (_get_animal_on_position(Point(1, 0))),
                       Point(0, 1): (_get_animal_on_position(Point(0, 1)))}
        world.create_random_plant()
        self.assertEqual(len(world.plants), 1)
        self.assertEqual(len(world.tiles), 4)
        self.assertTrue(isinstance(world.tiles[Point(1, 1)], Plant))

        world = Map(width=2, height=2)
        world.tiles = {Point(0, 0): (_get_animal_on_position(Point(0, 0))),
                       Point(1, 0): (_get_animal_on_position(Point(1, 0))),
                       Point(0, 1): (_get_animal_on_position(Point(0, 1))),
                       Point(1, 1): Plant(Point(1, 1), 10)}
        world.create_random_plant()
        self.assertEqual(len(world.plants), 1)
        self.assertEqual(len(world.tiles), 4)
        self.assertTrue(isinstance(world.tiles[Point(1, 1)], Plant))
        self.assertEqual(world.tiles[Point(1, 1)].energy, 10 + PLANT_ENERGY)

    def test_check_nearest_tiles_for_food(self):
        world = Map(width=2, height=2)
        world.tiles = {Point(0, 0): Plant(Point(0, 0), 3),
                       Point(0, 1): (_get_animal_on_position(Point(0, 1))),
                       Point(1, 1): Plant(Point(1, 1), 10)}
        new_position = world.check_nearest_tiles_for_food(Point(1, 0))
        self.assertEqual(new_position, Point(1, 1))

        world = Map(width=2, height=2)
        world.tiles = {Point(0, 0): (_get_animal_on_position(Point(0, 0))),
                       Point(0, 1): (_get_animal_on_position(Point(0, 1)))}
        new_position = world.check_nearest_tiles_for_food(Point(1, 0))
        self.assertEqual(new_position, Point(1, 0))

        world = Map(width=2, height=2)
        new_position = world.check_nearest_tiles_for_food(Point(1, 0))
        self.assertEqual(new_position, Point(1, 0))

    def test_find_food_or_die(self):
        world = Map(width=2, height=2)
        animal = _get_animal_on_position_with_energy(Point(1, 0), 0)
        plant1 = Plant(Point(0, 0), ENERGY_DEMAND_PER_ROUND)
        plant2 = Plant(Point(1, 1), ENERGY_DEMAND_PER_ROUND + 2)
        world.tiles = {Point(0, 0): plant1,
                       Point(1, 0): animal,
                       Point(0, 1): (_get_animal_on_position(Point(0, 1))),
                       Point(1, 1): plant2}
        world.plants = [plant1, plant2]
        world.find_food_or_die(animal)
        self.assertEqual(world.tiles[Point(1, 1)], animal)
        self.assertEqual(world.plants, [plant1])
        self.assertEqual(animal.energy, 2)
        self.assertEqual(animal.position, Point(1, 1))
        self.assertEqual(world.tiles.get(Point(1, 0)), None)

        world = Map(width=2, height=2)
        animal = _get_animal_on_position_with_energy(Point(1, 0), 0)
        plant = Plant(Point(0, 0), ENERGY_DEMAND_PER_ROUND)
        world.tiles = {Point(0, 0): plant,
                       Point(1, 0): animal}
        world.plants = [plant]
        world.find_food_or_die(animal)
        self.assertEqual(world.tiles[Point(0, 0)], animal)
        self.assertEqual(world.plants, [])
        self.assertEqual(animal.energy, 0)
        self.assertEqual(animal.position, Point(0, 0))
        self.assertEqual(world.tiles.get(Point(1, 0)), None)

        world = Map(width=2, height=2)
        animal = _get_animal_on_position_with_energy(Point(1, 0), 0)
        plant = Plant(Point(0, 0), ENERGY_DEMAND_PER_ROUND - 1)
        world.tiles = {Point(0, 0): plant,
                       Point(1, 0): animal}
        world.plants = [plant]
        world.animals = [animal]
        world.find_food_or_die(animal)
        self.assertEqual(world.plants, [])
        self.assertEqual(world.animals, [])
        self.assertEqual(world.tiles.get(Point(0, 0)), None)
        self.assertEqual(world.tiles.get(Point(1, 0)), None)

        world = Map(width=2, height=2)
        animal = _get_animal_on_position_with_energy(Point(1, 0), ENERGY_DEMAND_PER_ROUND - 1)
        world.tiles = {Point(1, 0): animal}
        world.animals = [animal]
        world.find_food_or_die(animal)
        self.assertEqual(world.plants, [])
        self.assertEqual(world.animals, [])
        self.assertEqual(world.tiles.get(Point(1, 0)), None)

    def test_kill_animal(self):
        world = Map(width=2, height=2)
        animal1 = _get_animal_on_position(Point(1, 0))
        animal2 = _get_animal_on_position(Point(0, 0))
        animal3 = _get_animal_on_position(Point(0, 1))
        world.tiles = {Point(0, 0): animal2,
                       Point(1, 0): animal1,
                       Point(0, 1): animal3}
        world.animals = [animal1, animal2, animal3]
        world.kill_animal(animal1)
        self.assertEqual(world.animals, [animal2, animal3])
        self.assertEqual(world.tiles.get(Point(1, 0)), None)

    def test_find_potential_partner(self):
        world = Map(width=2, height=2)
        animal1 = _get_animal_on_position_with_gender(Point(1, 0), Gender.F)
        animal2 = _get_animal_on_position_with_gender(Point(0, 0), Gender.M)
        animal3 = _get_animal_on_position_with_gender(Point(0, 1), Gender.F)
        animal4 = _get_animal_on_position_with_gender(Point(1, 1), Gender.M)
        world.tiles = {Point(0, 0): animal2,
                       Point(1, 0): animal1,
                       Point(0, 1): animal3,
                       Point(1, 1): animal4}
        partners = world.find_potential_partners(Point(1, 0), Gender.F)
        self.assertCountEqual(partners, [animal2, animal4])
        partners = world.find_potential_partners(Point(0, 0), Gender.M)
        self.assertCountEqual(partners, [animal1, animal3])

        world = Map(width=2, height=2)
        animal2 = _get_animal_on_position_with_gender(Point(0, 0), Gender.M)
        animal4 = _get_animal_on_position_with_gender(Point(1, 1), Gender.M)
        world.tiles = {Point(0, 0): animal2,
                       Point(1, 0): Plant(),
                       Point(0, 1): Plant(),
                       Point(1, 1): animal4}
        partners = world.find_potential_partners(Point(0, 0), Gender.M)
        self.assertEqual(partners, [])

    def test_find_other_animal_to_breed(self):
        world = Map(width=2, height=2)
        animal1 = Animal(Gender.F, Point(1, 0), Attributes(0.5, 0.5), 1, 2*BREED_ENERGY_FEMALE)
        animal2 = Animal(Gender.M, Point(0, 0), Attributes(0.7, 0.7), 1, BREED_ENERGY_MALE - 1)
        animal3 = Animal(Gender.M, Point(0, 1), Attributes(0.9, 0.9), 1, 2*BREED_ENERGY_MALE)
        animal4 = Animal(Gender.M, Point(1, 1), Attributes(0.7, 0.7), 1, 2*BREED_ENERGY_MALE)
        world.tiles = {Point(0, 0): animal2,
                       Point(1, 0): animal1,
                       Point(0, 1): animal3,
                       Point(1, 1): animal4}
        partners = world.find_other_animal_to_breed(animal1)
        self.assertEqual(len(partners), 1)
        self.assertEqual(partners[0], animal3)

        world = Map(width=2, height=2)
        animal1 = Animal(Gender.M, Point(1, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_MALE)
        animal2 = Animal(Gender.F, Point(0, 0), Attributes(0.7, 0.7), 1, BREED_ENERGY_FEMALE - 1)
        animal3 = Animal(Gender.F, Point(0, 1), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_FEMALE)
        animal4 = Animal(Gender.F, Point(1, 1), Attributes(0.7, 0.7), 1, 2 * BREED_ENERGY_FEMALE)
        world.tiles = {Point(0, 0): animal2,
                       Point(1, 0): animal1,
                       Point(0, 1): animal3,
                       Point(1, 1): animal4}
        partners = world.find_other_animal_to_breed(animal1)
        self.assertEqual(len(partners), 2)
        self.assertCountEqual(partners, [animal3, animal4])

    def test_find_partners_further(self):
        world = Map(width=2, height=3)
        animal1 = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_FEMALE)
        animal2 = Animal(Gender.M, Point(0, 2), Attributes(0.7, 0.7), 1, 2 * BREED_ENERGY_MALE)
        animal3 = Animal(Gender.M, Point(1, 2), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_MALE)
        world.tiles = {Point(0, 0): animal2,
                       Point(0, 2): animal1,
                       Point(1, 2): animal3}
        new_position = world.find_partners_further(animal1)
        self.assertEqual(new_position, Point(0, 1))

        world = Map(width=4, height=4)
        animal1 = Animal(Gender.F, Point(0, 2), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_FEMALE)
        animal2 = Animal(Gender.M, Point(3, 2), Attributes(0.7, 0.7), 1, 2 * BREED_ENERGY_MALE)
        animal3 = Animal(Gender.M, Point(0, 0), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_MALE)
        world.tiles = {Point(3, 2): animal2,
                       Point(0, 2): animal1,
                       Point(0, 0): animal3}
        new_position = world.find_partners_further(animal1)
        self.assertEqual(new_position, Point(1, 1))

        world = Map(width=4, height=4)
        animal1 = Animal(Gender.M, Point(0, 2), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_MALE)
        animal2 = Animal(Gender.F, Point(0, 0), Attributes(0.1, 0.1), 1, 2 * BREED_ENERGY_FEMALE)
        animal3 = Animal(Gender.F, Point(0, 1), Attributes(0.2, 0.2), 1, 2 * BREED_ENERGY_FEMALE)
        animal4 = Animal(Gender.F, Point(1, 0), Attributes(0.2, 0.2), 1, 2 * BREED_ENERGY_FEMALE)
        animal5 = Animal(Gender.F, Point(3, 1), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_FEMALE)
        animal6 = Animal(Gender.F, Point(3, 2), Attributes(0.8, 0.8), 1, 2 * BREED_ENERGY_FEMALE)
        world.tiles = {Point(0, 0): animal2,
                       Point(0, 2): animal1,
                       Point(0, 1): animal3,
                       Point(1, 0): animal4,
                       Point(3, 1): animal5,
                       Point(3, 2): animal6}
        new_position = world.find_partners_further(animal1)
        self.assertEqual(new_position, Point(1, 1))

    def test_get_position_next_to_most_attractive_partner(self):
        world = Map(width=3, height=3)
        animal1 = Animal(Gender.M, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_MALE)
        animal2 = Animal(Gender.M, Point(0, 1), Attributes(0.1, 0.1), 1, 2 * BREED_ENERGY_MALE)
        animal3 = Animal(Gender.M, Point(1, 0), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_MALE)
        animal4 = Animal(Gender.M, Point(2, 1), Attributes(0.2, 0.2), 1, 2 * BREED_ENERGY_MALE)
        position_partners_map = {Point(2, -1): [animal3],
                                 Point(1, 1): [animal1, animal2, animal3, animal4],
                                 Point(0, 2): [animal2],
                                 Point(2, 0): [animal3, animal4]}
        position = world.get_position_next_to_most_attractive_partner(position_partners_map)
        self.assertEqual(position, Point(1, 1))

        world = Map(width=3, height=3)
        animal1 = Animal(Gender.M, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_MALE)
        position_partners_map = {Point(-1, 0): [animal1]}
        position = world.get_position_next_to_most_attractive_partner(position_partners_map)
        self.assertEqual(position, None)

    def test_get_position_with_largest_number_of_females(self):
        world = Map(width=3, height=3)
        animal1 = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_FEMALE)
        animal2 = Animal(Gender.F, Point(0, 1), Attributes(0.1, 0.1), 1, 2 * BREED_ENERGY_FEMALE)
        animal3 = Animal(Gender.F, Point(0, 2), Attributes(0.9, 0.9), 1, 2 * BREED_ENERGY_FEMALE)
        position_partners_map = {Point(-1, -1): [animal1, animal2, animal3],
                                 Point(0, 1): [animal1, animal2],
                                 Point(2, 1): [animal2, animal3]}
        position = world.get_position_next_to_most_attractive_partner(position_partners_map)
        self.assertEqual(position, Point(2, 1))

        world = Map(width=3, height=3)
        animal1 = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_FEMALE)
        position_partners_map = {Point(-1, 0): [animal1]}
        position = world.get_position_next_to_most_attractive_partner(position_partners_map)
        self.assertEqual(position, None)

    def test_move_animal(self):
        world = Map(width=2, height=2)
        animal = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, 2 * BREED_ENERGY_FEMALE)
        world.tiles = {Point(0, 0): animal}
        world.move_animal(animal, Point(-1, -1))
        self.assertEqual(world.tiles.get(Point(0, 0)), animal)
        world.move_animal(animal, None)
        self.assertEqual(world.tiles.get(Point(0, 0)), animal)
        world.move_animal(animal, Point(1, 1))
        self.assertEqual(world.tiles.get(Point(0, 0)), None)
        self.assertEqual(world.tiles.get(Point(1, 1)), animal)

    def test_find_tile_with_largest_amount_of_food(self):
        world = Map(width=2, height=2)
        plant1 = Plant(Point(1, 0), 15)
        plant2 = Plant(Point(0, 1), 10)
        plant3 = Plant(Point(1, 1), 5)
        world.tiles = {Point(1, 0): plant1,
                       Point(0, 1): plant2,
                       Point(1, 1): plant3}
        position, max_energy = world.find_tile_with_largest_amount_of_food(Point(0, 0))
        self.assertEqual(position, Point(1, 0))
        self.assertEqual(max_energy, 15)

        world = Map(width=2, height=2)
        world.tiles = {}
        position, max_energy = world.find_tile_with_largest_amount_of_food(Point(0, 0))
        self.assertEqual(position, None)
        self.assertEqual(max_energy, 0)

    def test_find_food_further(self):
        world = Map(width=4, height=4)
        plant1 = Plant(Point(2, 0), 5)
        plant2 = Plant(Point(3, 1), 10)
        plant3 = Plant(Point(2, 3), 15)
        world.tiles = {Point(2, 0): plant1,
                       Point(3, 1): plant2,
                       Point(2, 3): plant3}
        position = world.find_food_further(Point(1, 1))
        self.assertEqual(position, Point(1, 2))

        world = Map(width=2, height=2)
        world.tiles = {}
        position = world.find_food_further(Point(0, 0))
        self.assertEqual(position, Point(0, 1))

    def test_get_free_neighbour_position(self):
        world = Map(width=2, height=2)
        world.tiles = {}
        position = world.get_free_neighbour_position(Point(0, 0))
        self.assertEqual(position, Point(0, 1))

        world = Map(width=2, height=2)
        world.tiles = {Point(0, 1): _get_animal_on_position(Point(0, 1)),
                       Point(1, 1): _get_animal_on_position(Point(1, 1))}
        position = world.get_free_neighbour_position(Point(0, 0))
        self.assertEqual(position, Point(1, 0))

        world = Map(width=2, height=2)
        world.tiles = {Point(0, 1): _get_animal_on_position(Point(0, 1)),
                       Point(1, 1): _get_animal_on_position(Point(1, 1)),
                       Point(1, 0): _get_animal_on_position(Point(1, 0))}
        position = world.get_free_neighbour_position(Point(0, 0))
        self.assertEqual(position, Point(0, 0))
