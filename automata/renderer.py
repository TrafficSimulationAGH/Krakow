"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plotter:
    """
    Plot wrapper for map drawing
    mapdata - MapData object
    updatef - update function f(frame)
    """

    def __init__(self, mapdata, updatef):
        self.osmap = mapdata
        self.updatef = updatef

    def blank(self):
        "Initialize map plot"
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim(*self.osmap.bbox['x'])
        self.ax.set_ylim(*self.osmap.bbox['y'])
        self.osmap.plot()

    def update(self, frame):
        self.updatef(frame)
        return plt.plot([20.5], [49.5])

    def render(self):
        "Show map plot"
        anim = FuncAnimation(self.fig, self.update, frames=range(0,4), blit=False, interval=1000)
        plt.show()

class MapData:
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

    def plot(self):
        "Plot roads"
        for road in self.roads:
            geom = road['geometry']
            if len(geom['coordinates']) > 0 and geom['type'] == 'LineString':
                coords = geom['coordinates']
                xs = [i[0] for i in coords]
                ys = [i[1] for i in coords]
                plt.plot(xs, ys, self.COLOR)
