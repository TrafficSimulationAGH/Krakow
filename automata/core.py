"""
Core definitions, basic structures.
"""
from random import choices
from math import sin, cos, sqrt, atan2, radians
import json
import pandas as pd

class OSM:
    """
    Map information wrapper
    HIGHWAY defines osm highway filters
    """
    HIGHWAY = ['primary', 'motorway', 'proposed', 'trunk', 'primary_link', 'motorway_link', 'trunk_link', 'give_way', 'motorway_junction']
    COLOR = 'b'

    def __init__(self, jsonfile=None):
        if jsonfile is not None:
            with open(jsonfile, 'r', encoding = 'utf-8') as f:
                json = f.read()
            self.load(json)

    def filter(self, func):
        """
        Filter out roads.
        func: item -> bool
        """
        return list(filter(func, self.roads))

    def load(self, json):
        "Load and filter data"
        def f(i):
            if 'highway' in i['properties']:
                precond = i['properties']['highway'] in self.HIGHWAY
                if 'proposed' in i['properties']:
                    return precond and i['properties']['proposed'] in self.HIGHWAY
                return precond
            else:
                return False
        data = eval(json)
        bbox = data['bbox']
        self.bbox = {'x': (bbox[0], bbox[2]), 'y': (bbox[1], bbox[3])}
        self.roads = data['features']
        self.roads = self.filter(f)

class Coords:
    """
    Geographical coordinates.
    """

    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)

    def dist(self, other):
        "Distance to other location"
        R = 6373000.0
        dlon = radians(self.lon - other.lon)
        dlat = radians(self.lat - other.lat)
        
        a = sin(dlat / 2)**2 + cos(radians(other.lat)) * cos(radians(self.lat)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        return round(distance)

class Cell:
    """
    Cell links: front, back, left, right
    Road cell containing information about:
    - probability of entering (for junctions)
    - location
    - vehicle inside
    - adjacent cells
    - road information dict
    """

    def __init__(self, coords, info=None):
        self.info = {}
        if info is not None:
            self.info = info
        self.probability = 0.5
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
        