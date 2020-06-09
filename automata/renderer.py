"""
Render a map and simulation elements.
Uses plotly for interactive plotting.
"""
import pandas as pd
import plotly.express as px
from automata.osmplotter import OSMPlotter

class AgentPlotter:
    """
    Plot wrapper for agents statistics.
    Interactive plotly graph.
    data - agent log
    """

    def __init__(self, data):
        self.df = data

class CellularPlotter:
    """
    Plot wrapper for simulation cells.
    Interactive plotly graph.
    data - cell log
    """

    def __init__(self, data):
        self.df = data

    def plot(self):
        "Create animated scatter figure."
        iters = len(self.df['iteration'].value_counts())
        if iters > 1:
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes'], animation_frame='iteration')
        else:
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes'])
