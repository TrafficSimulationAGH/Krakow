"Module containing static map definitions"
import math
import numpy as np

class Road:
    """
    Road contains points describing road shape.
    Destination is stored in a tuple.
    Points should be given in clockwise direction.
    """

    def __init__(self, start, dest, points, lanes=1):
        self.destination = (start, dest)
        self.points = np.array(points)
        self.lanes = lanes

    def clockwise(self):
        "Coordinates in clockwise direction"
        return self.points

    def anticlockwise(self):
        "Coordinates in anti-clockwise direction"
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
        keys = list(self.data.keys())
        self.roads = [None] * len(keys)
        for i in range(0,len(keys)):
            k = keys[i]
            a,b = k.split(';')
            self.roads[i] = Road(a, b, self.data[k]['geometry'], self.data[k]['lanes'])

    def save(self, fp):
        "Save data to file"
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(str(self.data))
