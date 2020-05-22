from unittest import TestCase
from . import mock
import automata.core as core

class TestCoords(TestCase):
    def test_init(self):
        c = core.Coords(23.0, 50)
        self.assertIs(type(c.lat), float)
        self.assertIs(type(c.lon), float)
        self.assertAlmostEqual(c.lat, 23.0)
        self.assertAlmostEqual(c.lon, 50.0)

    def test_dist(self):
        a = core.Coords(10.0, 10.0)
        b = core.Coords(11.0, 9.0)
        result = 155.99 #km
        self.assertAlmostEqual(a.dist(b) / 1000, result)
        self.assertAlmostEqual(b.dist(a) / 1000, result)
        self.assertAlmostEqual(b.dist(b), 0.0)

class TestCell(TestCase):
    def test_getitem(self):
        x = core.Cell(None)
        x.add(core.Cell(None))
        self.assertIsNone(x.adj['back'])
        self.assertIsNotNone(x.adj['front'])

    def test_add(self):
        x = core.Cell(None)
        x.add(core.Cell(None))
        x.add(core.Cell(None))
        last = x['front']['front']
        self.assertIsNotNone(last)
        self.assertIsNone(last['front'])

    def test_is_free(self):
        x = core.Cell(None)
        self.assertTrue(x.is_free())
        x.vehicle = core.Vehicle(1)
        self.assertFalse(x.is_free())

class TestVehicle(TestCase):
    def test_randomize(self):
        vh = core.Vehicle(5)
        vh.P = 1.0
        vh.V_MAX = 6
        vh.randomize()
        self.assertNotEqual(vh.v, 5)

    def test_step(self):
        road = mock.MockStraightRoad()
        car = core.Vehicle(1)
        road.start.set_vehicle(car)
        car.step()
        self.assertTrue(road.start.is_free())
        self.assertFalse(road.start['front'].is_free())
        self.assertTrue(road.start['front']['front'].is_free())
