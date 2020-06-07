from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import automata.utils as utils

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

class Plotter:
    """
    Plot wrapper for map drawing
    mapdata - MapData object
    """
    COLOR = 'b'

    def __init__(self, mapdata):
        self.osmap = mapdata
        self.anim = None
        self.fig = None
        self.ax = None

    def plot(self):
        "Initialize map plot. Uses self.fig and self.ax"
        if self.fig is None:
            self.fig = plt.figure()
            self.ax = None
        if self.ax is None:
            self.ax = self.fig.add_subplot()
        self.ax.set_xlim(*self.osmap.bbox['x'])
        self.ax.set_ylim(*self.osmap.bbox['y'])
        plot_elements(self.osmap.roads, self.COLOR)

    def cell_grid(self, grid):
        "Plot cells depending on its contents"
        ln = []
        ln.append(utils.plot_cells(grid, clr='go', ax=self.ax))
        ln.append(utils.plot_cells([x for x in grid if not x.is_free()], clr='ro', ax=self.ax))
        return ln

    def animation(self, cellular):
        "Show animation"
        art = self.cell_grid(cellular.array)
        self.anim = ArtistAnimation(self.fig, art, interval=500, blit=True)

    def show(self):
        "Show map plot"
        plt.show()
        self.fig = None

class OSM:
    """
    Map information wrapper
    HIGHWAY defines osm highway filters
    """
    HIGHWAY = ['primary', 'motorway', 'proposed', 'trunk', 'primary_link', 'motorway_link', 'trunk_link', 'give_way', 'motorway_junction']

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

def plot_elements(data, clr='b', ax=None, point='x'):
    "Plot list of road elements"
    for road in data:
        geom = road['geometry']
        if len(geom['coordinates']) > 0:
            coords = geom['coordinates']
            if type(coords[0]) is float:
                xs = [coords[0]]
                ys = [coords[1]]
            else:
                xs = [i[0] for i in coords]
                ys = [i[1] for i in coords]
            mark = '' if len(xs) > 1 else point
            if ax is None:
                plt.plot(xs, ys, clr + mark)
            else:
                ax.plot(xs, ys, clr + mark)
