"Module containing static map definitions"
import numpy as np

class Road:
    """
    Road contains points describing road shape.
    Points should be given in clockwise direction.
    """

    def __init__(self, points, lanes=1):
        self.points = points
        self.lanes = lanes

    def clockwise(self):
        return self.points

    def anticlockwise(self):
        return list(reversed(self.points))

class SM:
    """
    Static Map - contains information about roads on map.
    Allows loading from file.
    """

    def __init__(self, jsonfile=None):
        if jsonfile is not None:
            with open(jsonfile, 'r', encoding = 'utf-8') as f:
                json = f.read()
            self.load(json)

    def load(self, json):
        "Load data from json text"
        self.data = eval(json)
        pass

    def save(self, f):
        "Save data to file"
        pass
