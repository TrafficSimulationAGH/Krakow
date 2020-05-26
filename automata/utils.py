"""
Utility functions and classes definitions.
"""
import numpy as np
import matplotlib.pyplot as plt

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
