from unittest import TestCase
from . import mock
import automata.utils as utils

class TestCoords(TestCase):
    def test_init(self):
        c = utils.Coords(23.0, 50)
        self.assertIs(type(c.lat), float)
        self.assertIs(type(c.lon), float)
        self.assertAlmostEqual(c.lat, 23.0)
        self.assertAlmostEqual(c.lon, 50.0)

    def test_dist(self):
        a = utils.Coords(10.0, 10.0)
        b = utils.Coords(11.0, 9.0)
        result = 155.99 #km
        self.assertAlmostEqual(a.dist(b) / 1000, result)
        self.assertAlmostEqual(b.dist(a) / 1000, result)
        self.assertAlmostEqual(b.dist(b), 0.0)