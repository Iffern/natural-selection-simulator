import unittest

from components.attributes import Attributes
from config import COLOR, TAIL


class AttributesTest(unittest.TestCase):

    def test_get_random_attributes(self):
        attributes = Attributes.get_random_attributes()
        self.assertGreater(attributes.color, COLOR['min'])
        self.assertLess(attributes.color, COLOR['max'])
        self.assertGreater(attributes.tail, TAIL['min'])
        self.assertLess(attributes.tail, TAIL['max'])
