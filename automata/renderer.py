"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import automata.utils as utils

class Plotter:
    """
    Plot wrapper for map drawing
    mapdata - MapData object
    updatef - update function f(frame)
    """

    def __init__(self, mapdata, updatef):
        self.osmap = mapdata
        self.updatef = updatef

    def update(self, frame):
        self.updatef(frame)
        return plt.plot([20.5], [49.5], 'ro')

    def plot(self):
        "Initialize map plot"
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim(*self.osmap.bbox['x'])
        self.ax.set_ylim(*self.osmap.bbox['y'])
        utils.plot_map(self.osmap)

    def show(self):
        "Show map plot"
        anim = FuncAnimation(self.fig, self.update, frames=range(0,4), blit=False, interval=1000)
        plt.show()