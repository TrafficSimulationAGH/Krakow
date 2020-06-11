"""
Automata - a traffic simulation package.
Imports: numpy, matplotlib
"""
import sys
from . import config
from . import core
from . import utils
from . import stats
from . import renderer
from . import simplemap
from . import openmap

def simulate(maxsteps):
    # Initiate simulation
    sm = simplemap.SM('krakow.json')
    cellular = core.Cellular()
    cellular.build(sm)
    cstat = stats.LastCellStat()
    astat = stats.AgentStat()
    fstat = stats.InOutFlowStat()
    # Simulate
    for i in range(0,maxsteps):
        cellular.step([cstat, astat, fstat])
    # Return logs
    return cstat, astat, fstat

def main(maxsteps=200):
    cstat, astat, fstat = simulate(maxsteps)
    # Plot map
    plotter = renderer.CellularMap(cstat.log)
    fig = plotter.plot()
    fig.show()
    # Plot metrics
    metrics = renderer.AgentMetrics(astat.log)
    fig = metrics.plot()
    fig.show()
    # Plot flow
    log = fstat.log.drop('crossing', axis=1).groupby(['iteration','type']).sum().reset_index()
    flow = renderer.FlowMetrics(log)
    fig = flow.plot()
    fig.show()

if __name__ == "__main__":
    main()
