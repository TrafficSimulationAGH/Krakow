"Module containing static map definitions"
import numpy as np

class Road:
    """
    Road contains points describing road shape.
    Points should be given in clockwise direction.
    """

    def __init__(self, points, lanes=1, is_cw=True, is_acw=True):
        self.points = points
        self.lanes = lanes
        self.is_clockwise = is_cw
        self.is_anticlockwise = is_acw

    def clockwise(self):
        return self.points

    def anticlockwise(self):
        return list(reversed(self.points))

class SM:
    """
    Static Map - contains information about roads on map.
    Allows loading from file.
    """

    def __init__(self, npyfile=None):
        if npyfile is not None:
            self.load(npyfile)

    def load(self, f):
        "Load data from numpy file."
        self.data = np.load(f)
        self.roads = [Road(x[0], x[1]) for x in self.data]

    def save(self, f):
        np.save(f, self.data, allow_pickle=False)
