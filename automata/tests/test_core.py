import os
from unittest import TestCase
from . import mock
import automata.core as core

class TestCellular(TestCase):
    def test_build(self):
        builder = core.Cellular()
        builder.build(mock.MockJsonMap)
        self.assertSequenceEqual(mock.MockCellularMap.array, builder.array)

    def test_saveload(self):
        mock.MockCellularMap.save('temporary.json')
        fromfile = core.Cellular()
        fromfile.load('temporary.json')
        self.assertSequenceEqual(fromfile.array, mock.MockCellularMap.array)
        os.remove('temporary.json')

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

class TestSpawnPoint(TestCase):
    def test_spawn(self):
        sp = core.SpawnPoint([0.0, 0.0])
        sp.P = 1.0
        fst = sp.is_free()
        sp.spawn()
        snd = not sp.is_free()
        self.assertTrue(fst and snd)

        sp.set_vehicle(None)
        fst = sp.is_free()
        sp.P = 0.0
        sp.spawn()
        snd = sp.is_free()
        self.assertTrue(fst and snd)

class TestVehicle(TestCase):
    def test_randomize(self):
        vh = core.Vehicle(5)
        vh.P = 1.0
        vh.V_MAX = 6
        vh.randomize()
        self.assertNotEqual(vh.v, 5)

    def test_step(self):
        road = mock.MockStraightRoad
        car = core.Vehicle(1)
        road.set_vehicle(car)
        car.step()
        self.assertTrue(road.is_free())
        self.assertFalse(road['front'].is_free())
        self.assertTrue(road['front']['front'].is_free())
