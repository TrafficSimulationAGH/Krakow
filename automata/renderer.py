"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import automata.utils as utils
import automata.openmap as openmap

class SMPlotter:
    """
    Plot wrapper for StaticMap.
    Interactive cellular plot.
    """

    def __init__(self):
        pass

class OSMPlotter:
    """
    Plot wrapper for OSM map drawing
    mapdata - MapData object
    """
    COLOR = 'b'

    def __init__(self, mapdata):
        self.osmap = mapdata
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
        openmap.plot_elements(self.osmap.roads, self.COLOR)

    def cell_grid(self, grid):
        "Plot cells depending on its contents"
        ln = []
        ln.append(utils.plot_cells(grid, clr='go', ax=self.ax))
        ln.append(utils.plot_cells([x for x in grid if not x.is_free()], clr='ro', ax=self.ax))
        return ln

    def show(self):
        "Show map plot"
        plt.show()
        self.fig = None
