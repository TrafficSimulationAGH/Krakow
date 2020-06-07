"""
Core definitions, basic structures.
"""
from automata.openmap import OSM
from random import choices, random
import math
import numpy as np
import pandas as pd

class Vehicle:
    """
    Static variables:
    V_MAX - maximum speed
    P - probability of braking
    """
    V_MAX = 10
    P = 0.05

    def __init__(self, v):
        self.v = v
        self.cell = None

    def randomize(self):
        "Change variables randomly"
        if self.v > 1:
            if random() < self.P:
                self.v -= 1
        if self.v < self.V_MAX and random() < self.P:
            self.v += 1

    def step(self):
        "Move forward"
        self.randomize()
        n = self.v
        while n > 0:
            n -= 1

class Cell:
    """
    Cell links: front, back, left, right
    Road cell containing information about:
    - chance of entering (for junctions)
    - location
    - vehicle inside
    - adjacent cells
    - road information dict
    """

    def __init__(self, coords, info=None):
        self.chance = 1.0
        self.info = {}
        if info is not None:
            self.info = info
        self.coords = np.array(coords)
        self.vehicle = None
        self.adj = {'front':None, 'back':None, 'left':None, 'right':None}

    def __getitem__(self, key):
        return self.adj[key]

    def __eq__(self, other):
        if other is None:
            return False
        return (self.coords == other.coords).all()

    def __repr__(self):
        return '<automata.core.Cell c{0}-{1}>'.format(len(self), self.is_free())

    def __len__(self):
        connections = 0
        for k in self.adj:
            if self.exists(k):
                connections += 1
        return connections

    def heading(self):
        for k in ['front', 'back', 'left', 'right']:
            if self.exists(k):
                other = self.adj[k]
                vector = other.coords - self.coords
                heading = math.atan2(vector[1], vector[0])
                if k == 'back':
                    heading += math.pi
                elif k == 'right':
                    heading += math.pi / 2
                elif k == 'left':
                    heading -= math.pi / 2
                return heading
            else:
                return 0.0

    def speed_limit(self):
        # TODO: get limit
        return 10

    def lanes(self):
        return int(self.info['lanes'])

    def connections(self):
        "List of adjacency keys with not None connections"
        return [k for k in self.adj if self.adj[k] is not None]

    def exists(self, key):
        "Check if the cell is linked with another"
        return key in self.connections()

    def add(self, cell, key='front', okey='back'):
        "Add cell under a key. Self is assigned on next cell under okey - to disable use okey=None"
        if self.exists(key):
            self.adj[key].add(cell, key, okey)
        else:
            self.adj[key] = cell
            if okey is not None:
                cell.adj[okey] = self

    def set_vehicle(self, vehicle):
        "Set pointers for cell and vehicle."
        self.vehicle = vehicle
        if self.vehicle is not None:
            self.vehicle.cell = self

    def is_free(self):
        "Checks whether cell contains vehicle"
        return self.vehicle is None

    def copy(self):
        cell = Cell(self.coords, self.info)
        cell.adj = self.adj
        cell.chance = self.chance
        cell.heading = self.heading
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
    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)

    def __repr__(self):
        return '<automata.core.DeadPoint c{0}-{1}>'.format(len(self), self.is_free())

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

    """
    RATE = 0.3

    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)

    def __repr__(self):
        return '<automata.core.SpawnPoint c{0}-{1}>'.format(len(self), self.is_free())

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
    Cells grid projected on OSM map.
    Stores data in an array of Cells connected with their adj tables.
    """
    RADIUS = 1e-4
    
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

    def build(self, data:OSM):
        """ Construct cellular grid from OSM object """
        # Useful properties:
        # lanes turn:lanes :forward :backward
        # oneway junction
        # maxspeed maxspeed:hgv:conditional overtaking
        # destination destination:lanes destination:symbol:lanes
        pass
        
    def save(self, path):
        """ Save array to file """
        for i in range(0,self.array):
            self.array[i].id = i
        dump = [{'id':cell.id, 'info':cell.info, 'coords':cell.coords.tolist(), 'chance':cell.chance, 'adj':{k:cell[k].id for k in cell.adj}} for cell in self.array]
        df = pd.DataFrame(dump)
        df = df.set_index('id')
        df.to_csv(path, sep=';')

    def load(self, path):
        """ Load map from file """
        df = pd.read_csv(path, sep=';', index_col=0)
        self.array = [Cell(eval(x[1]), eval(x[0])) for x in df.values]
        for i in range(0,len(self.array)):
            self.array[i].chance = df.loc[i,'chance']
            adj = eval(df.loc[i,'adj'])
            for k in adj:
                if k != 'back' and adj[k] is not None:
                    self.array[i].add(self.array[adj[k]], k)
        