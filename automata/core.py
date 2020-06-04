"""
Core definitions, basic structures.
"""
from automata.openmap import OSM
from random import choices, random
import numpy as np
import pandas as pd

class Vehicle:
    """
    Static variables:
    V_MAX - maximum speed
    P - probability of braking/accelerating
    A - overtaking agression
    """
    V_MAX = 10
    P = 0.05
    A = 0.9

    def __init__(self, v):
        self.v = v
        self.cell = None

    def randomize(self):
        "Change variables randomly"
        if self.v > 1:
            self.v = choices([self.v, self.v-1], [1-self.P, self.P])

    def step(self):
        "Move forward"
        # TODO: do not move only front
        if self.cell['front'].is_free():
            self.cell['front'].vehicle = self
            self.cell.vehicle = None
            self.cell = self.cell['front']

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
    ADJ = ('front', 'back', 'left', 'right')

    def __init__(self, coords, info=None):
        self.info = {}
        if info is not None:
            self.info = info
        self.chance = 1.0
        self.coords = np.array(coords)
        self.vehicle = None
        self.front = None
        self.back = None
        self.left = None
        self.right = None
    
    def __setitem__(self, key, value):
        if key in self.ADJ:
            setattr(self, key, value)

    def __getitem__(self, key):
        if key in self.ADJ:
            return getattr(self, key)
        return None

    def __eq__(self, other):
        if other is None:
            return False
        return (self.coords == other.coords).all()

    def __repr__(self):
        return '<automata.core.Cell c{0}-{1}>'.format(len(self), self.is_free())

    def __len__(self):
        connections = 0
        for k in self.ADJ:
            if self.exists(k):
                connections += 1
        return connections

    def step(self):
        "Perform simulation step - call step if needed"
        if self.vehicle is not None:
            self.vehicle.step()

    def exists(self, key):
        "Check if the cell is linked with another"
        return self[key] is not None

    def add(self, cell, key='front', okey='back'):
        "Add cell under a key. Self is assigned on next cell under okey - to disable use okey=None"
        if self.exists(key):
            self[key].add(cell, key, okey)
        else:
            self[key] = cell
            if okey is not None:
                cell[okey] = self

    def set_vehicle(self, vehicle):
        "Set pointers for cell and vehicle"
        if vehicle is not None:
            vehicle.cell = self
        self.vehicle = vehicle

    def is_free(self):
        "Is cell available"
        return self.vehicle is None

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
        if vehicle is not None:
            del vehicle

    @staticmethod
    def from_cell(cell: Cell):
        dp = DeadPoint(cell.coords, cell.info)
        for k in dp.ADJ:
            dp[k] = cell[k]
        dp.chance = cell.chance
        return dp

class SpawnPoint(Cell):
    """
    Cell derived class that populates itself with vehicles.
    P - probability of spawning
    """
    P = 0.3

    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)

    def __repr__(self):
        return '<automata.core.SpawnPoint c{0}-{1}>'.format(len(self), self.is_free())

    def step(self):
        "Perform simulation step - spawn"
        super().step()
        self.spawn()

    def spawn(self):
        "Spawn a vehicle with a random chance. Only if empty."
        if not self.is_free():
            return
        if random() < self.P:
            self.set_vehicle(Vehicle(2))

    @staticmethod
    def from_cell(cell: Cell):
        sp = SpawnPoint(cell.coords, cell.info)
        for k in sp.ADJ:
            sp[k] = cell[k]
        sp.chance = cell.chance
        sp.set_vehicle(cell.vehicle)
        return sp

class Cellular:
    """
    Cells grid projected on OSM map.
    Stores data in an array of Cells connected with their adj tables.
    """
    STEP = 0.0002
    
    def __init__(self):
        self.array = []

    def step(self):
        for x in self.array:
            x.step()

    # TODO: use constant step to generate cells
    def build(self, data:OSM):
        """ Construct cellular grid from OSM object """
        # Useful properties:
        # lanes turn:lanes :forward :backward
        # oneway junction
        # maxspeed maxspeed:hgv:conditional overtaking
        # destination destination:lanes destination:symbol:lanes
        df = pd.DataFrame(data.roads)
        df2 = pd.DataFrame(data=df['geometry'].tolist(), index=df.index)
        for i in df.index:
            if 'Line' in df2.loc[i,'type']:
                self.array += [Cell(c, info=df.loc[i,'properties']) for c in df2.loc[i,'coordinates']]
        
    def save(self, path):
        """ Save array to file """
        dump = [{'info':cell.info, 'coords':cell.coords.tolist(), 'chance':cell.chance, 'adj':{}} for cell in self.array]
        df = pd.DataFrame(dump)
        # TODO: build adj dict basing on df index
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
        