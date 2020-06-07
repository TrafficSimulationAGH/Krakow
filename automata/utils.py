"""
Utility functions and classes definitions.
"""
import numpy as np
import matplotlib.pyplot as plt

def plot_cells(cells, clr='ro', ax=None):
    coords = np.array([np.array(c.coords) for c in cells])
    if len(coords) < 1:
        return None
    if ax is None:
        ln = plt.plot(*coords.T, clr)
    else:
        ln = ax.plot(*coords.T, clr)
    return ln
