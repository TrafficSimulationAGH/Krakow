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
        # TODO: call randomize
        # TODO: use other options than front as well
        # TODO: use speed v
        if self.cell.exists('front') and self.cell.adj['front'].is_free():
            self.cell.set_vehicle(None)
            self.cell['front'].set_vehicle(self)

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
        self.info = {}
        if info is not None:
            self.info = info
        self.chance = 1.0
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

    def exists(self, key):
        "Check if the cell is linked with another"
        return self.adj[key] is not None

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
        "Is cell available"
        return self.vehicle is None

class DeadPoint(Cell):
    """
    Cell derived class that removes all vehicles that enter it.
    """
    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)

    def __init_subclass__(cls):
        return super().__init_subclass__()

    def __repr__(self):
        return '<automata.core.DeadPoint c{0}-{1}>'.format(len(self), self.is_free())

    def set_vehicle(self, vehicle):
        self.vehicle = None
        vehicle.cell = None

    @staticmethod
    def from_cell(cell: Cell):
        return DeadPoint(cell)

class SpawnPoint(Cell):
    """
    Cell derived class that populates itself with vehicles.
    P - probability of spawning
    """
    P = 0.3

    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)
    
    def __init_subclass__(cls):
        return super().__init_subclass__()

    def __repr__(self):
        return '<automata.core.SpawnPoint c{0}-{1}>'.format(len(self), self.is_free())

    def spawn(self):
        "Spawn a vehicle with a random chance. Returns spawned object."
        if self.is_free() and random() < self.P:
            self.set_vehicle(Vehicle(2))
            return self.vehicle
        return None

    @staticmethod
    def from_cell(cell: Cell):
        return SpawnPoint(cell)

class Cellular:
    """
    Cells grid projected on OSM map.
    Stores data in an array of Cells connected with their adj tables.
    """
    LANEVEC = np.array([0.0001, 0.0001])
    RADIUS = 0.0002
    
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
        df = pd.DataFrame(data.roads)
        df2 = pd.DataFrame(data=df['geometry'].tolist(), index=df.index)
        for i in df.index:
            if 'Line' in df2.loc[i,'type']:
                self.array += [Cell(c, info=df.loc[i,'properties']) for c in df2.loc[i,'coordinates']]
        
    def save(self, path):
        """ Save array to file """
        for i in range(0,self.array):
            self.array[i].id = i
        dump = [{'info':cell.info, 'coords':cell.coords.tolist(), 'chance':cell.chance, 'adj':{k:cell[k].id for k in cell.adj}} for cell in self.array]
        df = pd.DataFrame(dump)
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
        