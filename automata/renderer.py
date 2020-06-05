"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import automata.utils as utils

class Plotter:
    """
    Plot wrapper for map drawing
    mapdata - MapData object
    """

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
        utils.plot_elements(self.osmap.roads, self.osmap.COLOR)

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
