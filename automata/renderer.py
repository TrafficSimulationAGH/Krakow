"""
Render a map and simulation elements.
Uses plotly for interactive plotting.
"""
import pandas as pd
import plotly.express as px
from automata.osmplotter import OSMPlotter

class Plotter:
    """
    Abstract wrapper for plotting with plotly.
    data - log dataframe
    """

    def __init__(self, data):
        self.df = data
        self.cmap = px.colors.sequential.Plasma

    def plot(self):
        "Create animated scatter figure."
        iters = len(self.df['iteration'].value_counts())
        if iters > 1:
            return px.scatter(self.df, x='x', y='y', color_continuous_scale=self.cmap, animation_frame='iteration')
        else:
            return px.scatter(self.df, x='x', y='y', color_continuous_scale=self.cmap)

class AgentMetrics(Plotter):
    """
    Plot wrapper for agents statistics.
    Interactive plotly graph.
    data - agent log df
    """

    def plot(self):
        return super().plot()

class CellularMap(Plotter):
    """
    Plot wrapper for simulation map.
    Interactive plotly graph.
    data - cell log df
    """

    def plot(self):
        "Create animated scatter figure."
        iters = len(self.df['iteration'].value_counts())
        if iters > 1:
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes'],
                color_continuous_scale=self.cmap, animation_frame='iteration')
        else:
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes'],
                color_continuous_scale=self.cmap)
