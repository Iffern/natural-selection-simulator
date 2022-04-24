import unittest

from components.animal import Animal
from components.attributes import Attributes
from components.gender import Gender
from components.point import Point
from config import BREED_ENERGY_FEMALE, BREED_ENERGY_MALE, ENERGY_DEMAND_PER_ROUND

LOWER_LEFT = Point(-1, -1)
UPPER_RIGHT = Point(1, 1)


def _get_animal_on_position(position: Point):
    return Animal(Gender.F, position, Attributes(0.5, 0.5), 1, 0)


def _is_in_bounds(position: Point):
    return LOWER_LEFT <= position <= UPPER_RIGHT


class AnimalTest(unittest.TestCase):

    def test_move(self):
        initial_position = Point(0, 0)
        animal = Animal(Gender.F, initial_position, Attributes(0.5, 0.5), 1, 1)
        animal.move(Point(9, -7))
        self.assertEqual(animal.position, Point(9, -7))

    def test_can_breed(self):
        female = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, BREED_ENERGY_FEMALE - 1)
        male = Animal(Gender.M, Point(0, 0), Attributes(0.5, 0.5), 1, BREED_ENERGY_MALE - 1)
        self.assertFalse(female.can_breed())
        self.assertFalse(male.can_breed())
        female.energy = BREED_ENERGY_FEMALE
        male.energy = BREED_ENERGY_MALE
        self.assertTrue(female.can_breed())
        self.assertTrue(male.can_breed())

    def test_eat(self):
        animal = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, ENERGY_DEMAND_PER_ROUND)
        self.assertTrue(animal.eat())
        self.assertEqual(animal.energy, 0)
        self.assertFalse(animal.eat())

    def test_energy_for_breed(self):
        female = Animal(Gender.F, Point(0, 0), Attributes(0.5, 0.5), 1, BREED_ENERGY_FEMALE - 1)
        male = Animal(Gender.M, Point(0, 0), Attributes(0.5, 0.5), 1, BREED_ENERGY_MALE - 1)
        self.assertEqual(female.energy_for_breed(), BREED_ENERGY_FEMALE)
        self.assertEqual(male.energy_for_breed(), BREED_ENERGY_MALE)

    def test_get_child_position(self):
        point = Point(0, 0)
        tiles = {Point(0, 1): (_get_animal_on_position(Point(0, 1))),
                 Point(1, 1): (_get_animal_on_position(Point(1, 1))),
                 Point(1, 0): (_get_animal_on_position(Point(1, 0))),
                 Point(1, -1): (_get_animal_on_position(Point(1, -1))),
                 Point(0, -1): (_get_animal_on_position(Point(0, -1))),
                 Point(-1, -1): (_get_animal_on_position(Point(-1, -1))),
                 Point(-1, 0): (_get_animal_on_position(Point(-1, 0)))}
        self.assertEqual(Animal.get_child_position(point, tiles, _is_in_bounds), Point(-1, 1))

        tiles = {Point(0, 1): (_get_animal_on_position(Point(0, 1))),
                 Point(1, 1): (_get_animal_on_position(Point(1, 1))),
                 Point(1, 0): (_get_animal_on_position(Point(1, 0))),
                 Point(1, -1): (_get_animal_on_position(Point(1, -1))),
                 Point(0, -1): (_get_animal_on_position(Point(0, -1))),
                 Point(-1, -1): (_get_animal_on_position(Point(-1, -1))),
                 Point(-1, 0): (_get_animal_on_position(Point(-1, 0))),
                 Point(-1, 1): (_get_animal_on_position(Point(-1, 1)))}
        self.assertEqual(Animal.get_child_position(point, tiles, _is_in_bounds), Point(0, 0))


if __name__ == '__main__':
    unittest.main()
