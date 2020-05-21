"""
Utility functions and classes definitions.
"""
import numpy as np
import matplotlib.pyplot as plt

def plot_map(data):
    "Plot roads"
    for road in data.roads:
        geom = road['geometry']
        if len(geom['coordinates']) > 0 and geom['type'] == 'LineString':
            coords = geom['coordinates']
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            plt.plot(xs, ys, data.COLOR)
