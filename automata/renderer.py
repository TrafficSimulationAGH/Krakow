"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
# FuncAnimation might not work well
# Try blit
from matplotlib.animation import FuncAnimation
import automata.utils as utils

class Plotter:
    """
    Plot wrapper for map drawing
    mapdata - MapData object
    updatef - update function f(frame)
    """

    def __init__(self, mapdata):
        self.osmap = mapdata
        self.fig = None
        self.ax = None

    def update(self, frame):
        ax = None
        return ax

    def plot(self):
        "Initialize map plot. Uses self.fig and self.ax"
        if self.fig is None:
            self.fig = plt.figure()
            self.ax = None
        if self.ax is None:
            self.ax = self.fig.add_subplot()
        self.ax.set_xlim(*self.osmap.bbox['x'])
        self.ax.set_ylim(*self.osmap.bbox['y'])
        utils.plot_elements(self.osmap.roads, self.osmap.COLOR)

    def cell_grid(self, grid):
        "Plot cells depending on its contents"
        # TODO: check cell properties
        utils.plot_cells(grid, ax=self.ax)

    def show(self):
        "Show map plot"
        #anim = FuncAnimation(self.fig, self.update, frames=range(0,4), blit=False, interval=1000)
        plt.show()
        self.fig = None
