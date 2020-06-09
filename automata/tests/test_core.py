import os
from unittest import TestCase
from . import mock
import automata.core as core
import automata.utils as utils

class TestCell(TestCase):
    def test_is_free(self):
        x = core.Cell([0.0,0.0])
        self.assertTrue(x.is_free())
        x.set_vehicle(core.Vehicle(1))
        self.assertFalse(x.is_free())

class TestSpawnPoint(TestCase):
    def test_spawn(self):
        sp = core.SpawnPoint([0.0, 0.0])
        sp.RATE = 1.0
        fst = sp.is_free()
        sp.spawn()
        snd = not sp.is_free()
        self.assertTrue(fst and snd)

        sp.set_vehicle(None)
        fst = sp.is_free()
        sp.RATE = 0.0
        sp.spawn()
        snd = sp.is_free()
        self.assertTrue(fst and snd)

class TestVehicle(TestCase):
    def test_randomize(self):
        vh = core.Vehicle(5)
        vh.SLOW = 1.0
        vh.FAST = 0.0
        vh.LIMIT = 0.0
        vh.V_MAX = utils.vcell2speed(6)
        vh.randomize()
        self.assertNotEqual(vh.v, 5)
        vh.v = 1
        vh.randomize()
        self.assertEqual(vh.v, 1)

    def test_step(self):
        road = mock.MockStraightRoad
        car = core.Vehicle(1)
        car.SLOW = 0.0
        car.FAST = 0.0
        car.LIMIT = 0.0
        road.set_vehicle(car)
        car.step()
        self.assertTrue(road.is_free())
        self.assertFalse(road.forward.is_free())
        self.assertTrue(road.forward.forward.is_free())
