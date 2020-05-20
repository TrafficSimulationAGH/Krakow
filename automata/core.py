"""
Core definitions, basic structures.
"""

import random

class Cellular:
    """
    Cells grid projected on OSM map.
    """
    
    def __init__(self):
        pass

class OSM:
    """
    Map information wrapper
    HIGHWAY defines osm highway filters
    """
    HIGHWAY = ['primary', 'secondary', 'motorway', 'proposed', 'trunk', 'tertiary_link', 'primary_link', 'motorway_link', 'trunk_link', 'stop', 'bridleway', 'platform', 'construction', 'traffic_signals', 'turning_circle', 'give_way', 'motorway_junction']
    COLOR = 'b'

    def __init__(self, jsonfile=None):
        if jsonfile is not None:
            with open(jsonfile, 'r') as f:
                json = f.read()
            self.load(json)

    def load(self, json):
        "Load and filter data"
        def f(i):
            if 'highway' in i['properties']:
                return i['properties']['highway'] in self.HIGHWAY
            else:
                return False
        data = eval(json)
        bbox = data['bbox']
        self.bbox = {'x': (bbox[0], bbox[2]), 'y': (bbox[1], bbox[3])}
        self.roads = list(filter(f, data['features']))

class Coords:
    """
    Geographical coordinates.
    """

    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)

    def dist(self, other):
        "Distance to other location"
        return 0.0

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

    def __init__(self, coords):
        self.info = {}
        self.probability = 0.5
        self.coords = coords
        self.vehicle = None
        self.adj = {'front':None, 'back':None, 'left':None, 'right':None}

    def __getitem__(self, key):
        return self.adj[key]

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
            self.v = random.choices([self.v, self.v-1], [1-self.P, self.P])

    def step(self):
        "Move forward"
        pass
