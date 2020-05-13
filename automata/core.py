"""
Core definitions, basic structures.
"""

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
    """

    def __init__(self, coords, speed_limit=4):
        self.probability = 0.5
        self.speed_limit = speed_limit
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
        pass

    def step(self):
        "Move forward"
        pass
