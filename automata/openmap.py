import matplotlib.pyplot as plt
import automata.utils as utils

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
