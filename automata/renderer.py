"""
Render a map and simulation elements.
Uses plotly for interactive plotting.
"""
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from automata.osmplotter import OSMPlotter

class Plotter:
    """
    Abstract wrapper for plotting with plotly.
    data - log dataframe
    """

    def __init__(self, data):
        self.df = data
        self.cmap = px.colors.sequential.Burgyl

    def plot(self):
        "Create scatter figure."
        return px.scatter(self.df, x='x', y='y', color_continuous_scale=self.cmap)

class AgentMetrics(Plotter):
    """
    Plot wrapper for agents statistics.
    Interactive plotly graph.
    data - agent log df
    """

    def plot(self):
        "Plot metrics with interactive plotly graph."
        # Make dataframe
        data = []
        for i in range(0,self.df['iteration'].max()):
            grp = self.df[self.df['iteration'] == i]
            data.append({'iteration': i, 'cars': len(grp), 'km/h': grp['km/h'].mean()})
        df = pd.DataFrame(data)
        # Plot newly created dataframe
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        fig.add_trace(go.Scatter(x=df['iteration'], y=df['cars'], name='Agents count'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['iteration'], y=df['km/h'], name='Mean speed'), row=2, col=1)
        return fig

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
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes','type'],
                color_continuous_scale=self.cmap, animation_frame='iteration')
        else:
            return px.scatter(self.df, x='x', y='y', color='density', hover_data=['id','speed_lim','lanes','type'],
                color_continuous_scale=self.cmap)
