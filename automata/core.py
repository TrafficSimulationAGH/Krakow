"""
Core definitions, basic structures.
"""
from automata.openmap import OSM
from random import choices
import json
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
        if self.v > 0:
            self.v = choices([self.v, self.v-1], [1-self.P, self.P])

    def step(self):
        "Move forward"
        if self.cell.adj['front'].is_free():
            self.cell.adj['front'].vehicle = self
            self.cell.vehicle = None
            self.cell = self.cell.adj['front']

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
        self.coords = coords
        self.vehicle = None
        self.adj = {'front':None, 'back':None, 'left':None, 'right':None}

    def __getitem__(self, key):
        return self.adj[key]

    def __eq__(self, other):
        return self.coords == other.coords

    def __repr__(self):
        return '<automata.core.Cell ({0}:{1})>'.format(*self.coords)

    def exists(self, key):
        "Check if the cell is linked with another"
        return self.adj[key] is not None

    def add(self, cell, key='front'):
        "Add cell under a key"
        if self.exists(key):
            self.adj[key].add(cell, key)
        else:
            self.adj[key] = cell

    def set_vehicle(self, vehicle):
        "Set pointers for cell and vehicle"
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

    def set_vehicle(self, vehicle):
        self.vehicle = None
        vehicle.cell = None
        del vehicle

    @staticmethod
    def from_cell(cell: Cell):
        dp = DeadPoint(cell.coords, cell.info)
        dp.adj = cell.adj
        dp.chance = cell.chance
        return dp

class SpawnPoint(Cell):
    """
    Cell derived class that populates itself with vehicles.
    P - probability of spawning
    """
    P = 0.5

    def __init__(self, coords, info=None):
        super().__init__(coords, info=info)

    def spawn(self):
        "Spawn a vehicle with a random chance. Only if empty."
        pass

    @staticmethod
    def from_cell(cell: Cell):
        sp = SpawnPoint(cell.coords, cell.info)
        sp.adj = cell.adj
        sp.chance = cell.chance
        sp.set_vehicle(cell.vehicle)
        return sp

class Cellular:
    """
    Cells grid projected on OSM map.
    Stores data in an array of Cells connected with their adj tables.
    """
    
    def __init__(self):
        self.array = []

    def build(self, data:OSM):
        """ Construct cellular grid from OSM object """
        # Useful properties:
        # lanes turn:lanes :forward :backward
        # oneway junction
        # maxspeed maxspeed:hgv:conditional overtaking
        # destination destination:lanes destination:symbol:lanes
        
        df = pd.DataFrame(data.roads)
        df2 = pd.DataFrame(df['geometry'].values.tolist())
        for x in df2['coordinates']:
            if type(x[0]) is float:
                self.array.append(Cell(x, info=df['properties']))
            else:
                self.array += [Cell(c, info=df['properties']) for c in x]        
        
    def save(self, path):
        """ Save array to file """
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.array, file, default=lambda x: x.__dict__, ensure_ascii=False, indent=4)

    def load(self, path):
        """ Load map from file """
        with open(path, 'r', encoding = 'utf-8') as file:
            data = json.load(file)
            for x in data:
                self.array.append(Cell(x['coords'], info=x['info']))
        