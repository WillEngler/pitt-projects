import unittest
from diversity_experiment import split


class HelperTests(unittest.TestCase):
    def test_split(self):
        entire_range = range(0, 561)

        test_beginning = split(entire_range, 0, 5)
        self.assertEquals(test_beginning[0], range(112, 561))
        self.assertEquals(test_beginning[1], range(0, 112))

        test_middle = split(entire_range, 2, 5)
        self.assertEquals(test_middle[0], range(0, 224) + range(336, 561))
        self.assertEquals(test_middle[1], range(224, 336))

        test_end = split(entire_range, 4, 5)
        self.assertEquals(test_end[0], range(0,448))
        self.assertEquals(test_end[1], range(448,561))