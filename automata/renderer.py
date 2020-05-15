"""
Render a map and simulation elements.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MapPlot:
    """
    Plot wrapper for map drawing
    """

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.xdata = []
        self.ydata = []

    def update(self, frame):
        self.xdata.append(frame)
        self.ydata.append(frame**2.0)
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,

    def render(self):
        self.ln, = plt.plot([], [], 'ro')
        self.ax.set_xlim(-1, 5)
        self.ax.set_ylim(-1, 17)
        anim = FuncAnimation(self.fig, lambda f: self.update(f), frames=range(0,4), blit=False, interval=1000)
        plt.show()
