"""
Render a map and simulation elements.
Uses plotly for interactive plotting.
"""
import pandas as pd
import plotly.express as px
import automata.utils as utils
from automata.osmplotter import OSMPlotter

class StatsPlotter:
    """
    Plot wrapper for collected statistics.
    Interactive plotly graph.
    data - Statistics object
    """

    def __init__(self, data):
        self.stats = data

class CellularPlotter:
    """
    Plot wrapper for simulation cells.
    Interactive plotly graph.
    data - Cellular object
    """
    # TODO: animated plot

    def __init__(self, data):
        self.cells = data.array

    def plot(self):
        "Create scatter figure"
        to_dict = lambda x: {'x':x.coords[0],'y':x.coords[1],'id':x.id,'lanes':x.lanes,'density':round(x.vehicles/x.lanes,2),'speed_lim':x.speed_lim}
        data = [to_dict(x) for x in self.cells]
        df = pd.DataFrame(data)
        return px.scatter(df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes'])
