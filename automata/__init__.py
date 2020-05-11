"""
Automata - a traffic simulation package.

Imports: numpy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

def main():
    ax.set_xlim(0, 4)
    ax.set_ylim(-1.2, 1.2)
    anim = FuncAnimation(fig, update, frames=np.linspace(0,4), blit=True)
    plt.show()

if __name__ == "__main__":
    main()
