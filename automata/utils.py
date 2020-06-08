"""
Utility functions and classes definitions.
"""
from automata.config import CONFIG
import math
import numpy as np
import matplotlib.pyplot as plt

def plot_cells(cells, clr='ro', ax=None):
    coords = np.array([np.array(c.coords) for c in cells])
    if len(coords) < 1:
        return None
    if ax is None:
        ln = plt.plot(*coords.T, clr)
    else:
        ln = ax.plot(*coords.T, clr)
    return ln

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
        dlon = math.radians(self.lon - other.lon)
        dlat = math.radians(self.lat - other.lat)
        
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(other.lat)) * math.cos(math.radians(self.lat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return round(distance)

def vcell2speed(vcell):
    dst = Coords(0.0, 0.0).dist()
