"""
Render a map and simulation elements.
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import automata.utils as utils
import automata.openmap as openmap

class SimulationPlotter:
    """
    Plot wrapper for simulation cells.
    Interactive plotly graph.
    data - Cellular object
    """

    def __init__(self, data):
        self.agents = data.agents
        self.cells = data.array
        self.fig = None

    def plot(self):
        self.fig = go.Figure()
        data = [{'x':x.coords[0],'y':x.coords[1],'id':x.id,'lanes':x.lanes,'vehicles':x.vehicles,'speed_lim':x.speed_lim} for x in self.cells]
        df = pd.DataFrame(data)
        self.fig.add_trace(go.Scatter(df, mode='markers'))
        return self.fig

class OSMPlotter:
    """
    Plot wrapper for OSM map drawing
    mapdata - OpenStreetMap object
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
