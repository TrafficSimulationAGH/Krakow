"""
Core definitions, basic structures.
"""
import automata.utils as utils
import automata.staticmap as sm
from random import choices, random
import math
import numpy as np
import pandas as pd

class Vehicle:
    """
    Static variables:
    V_MAX - maximum speed (km/h)
    P - probability of braking
    """
    V_MAX = 10
    P = 0.05

    def __init__(self, v):
        self.v = v
        self.cell = None

    def randomize(self):
        "Change variables randomly"
        if self.v > 1 and random() < self.P:
            self.v -= 1
        elif self.v < self.V_MAX and random() < self.P:
            self.v += 1
        elif random() < self.P:
            self.v = min(self.cell.speed_lim, self.V_MAX)

    def step(self):
        "Move forward"
        self.randomize()
        n = self.v
        while n > 0:
            n -= 1

class Cell:
    """
    Road cell containing information about:
    - lanes
    - speed limit
    - coordinates
    - vehicle
    - adjacent cell
    """

    def __init__(self, coords, lanes=1, speed_lim=10):
        self.lanes = lanes
        self.speed_lim = speed_lim
        self.coords = np.array(coords)
        self.adj = None
        self.vehicle = None

    def __eq__(self, other):
        if other is None:
            return False
        return (self.coords == other.coords).all()

    def __repr__(self):
        return '<automata.core.Cell {0} {1}>'.format(self.coords, self.is_free())

    def heading(self):
        if self.adj is not None:
            vector = self.adj.coords - self.coords
            return math.atan2(vector[1], vector[0])

    def append(self, cell):
        "Set adjacent cell on first None adjacent pointer"
        if self.adj is None:
            self.adj = cell
        else:
            self.adj.append(cell)

    def set_vehicle(self, vehicle):
        "Set pointers for cell and vehicle."
        self.vehicle = vehicle
        if self.vehicle is not None:
            self.vehicle.cell = self

    def is_free(self):
        "Checks whether cell contains vehicle"
        return self.vehicle is None

    def copy(self):
        cell = Cell(self.coords, self.lanes, self.speed_lim)
        cell.adj = self.adj
        cell.__class__ = self.__class__
        return cell

    @staticmethod
    def from_point(point):
        point.__class__ = Cell
        return point

class DeadPoint(Cell):
    """
    Cell derived class that removes all vehicles that enter it.
    """
    def __repr__(self):
        return '<automata.core.DeadPoint {0} {1}>'.format(self.coords, self.is_free())

    def set_vehicle(self, vehicle):
        self.vehicle = None
        vehicle.cell = None

    @staticmethod
    def from_cell(cell: Cell):
        cell.__class__ = DeadPoint
        return cell

class SpawnPoint(Cell):
    """
    Cell derived class that populates itself with vehicles.
    RATE - probability of spawning
    """
    RATE = 0.3

    def __repr__(self):
        return '<automata.core.SpawnPoint {0} {1}>'.format(self.coords, self.is_free())

    def spawn(self):
        "Spawn a vehicle with a random chance. Returns spawned object."
        if self.is_free() and random() < self.RATE:
            self.set_vehicle(Vehicle(1))
            return self.vehicle
        return None

    @staticmethod
    def from_cell(cell: Cell):
        cell.__class__ = SpawnPoint
        return cell

class Cellular:
    """
    Simulation runner class.
    Loads config: RADIUS.
    """

    def __init__(self):
        self.agents = []
        self.array = []
        self.spawns = []

    def step(self):
        "Perform simulation step. Call spawners and agents."
        for x in self.spawns:
            v = x.spawn()
            if v is not None:
                self.agents.append(v)
        # Clear agents that do not exist on map
        self.agents = [x for x in self.agents if x.cell is not None]
        for x in self.agents:
            if x is None:
                continue
            x.step()

    def offset_lane(self, points, n):
        "Points moved perpendicularly to create new lane"
        vec = np.array(points[-1]) - np.array(points[0])
        heading = math.atan2(vec[1], vec[0]) + math.pi / 2
        vec = np.array([math.cos(heading), math.sin(heading)]) * utils.CONFIG.RADIUS * n
        return points + vec

    def build(self, data:sm.SM):
        "Construct cellular grid from SM object"
        pass
        