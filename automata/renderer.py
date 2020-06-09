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
    data - Stat object
    """

    def __init__(self, data):
        self.df = data.agent_log

class CellularPlotter:
    """
    Plot wrapper for simulation cells.
    Interactive plotly graph.
    data - Stat object
    """

    def __init__(self, data):
        self.df = data.cell_log

    def plot(self):
        "Create animated scatter figure."
        return px.scatter(self.df, x='x', y='y', color='density',
            animation_frame='iteration', hover_data=['id','speed_lim','lanes'])
