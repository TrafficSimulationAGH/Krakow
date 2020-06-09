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

def main():
    # Reduce resolution
    utils.CONFIG.RADIUS = 1e-4
    utils.CONFIG.TIMESTEP = 1.5
    # Initiate simulation
    sm = simplemap.SM('krakow.json')
    cellular = core.Cellular()
    cellular.build(sm)
    cstat = stats.LastCellStat()
    astat = stats.AgentStat('agent.log')
    fstat = stats.InOutFlowStat('flow.log')
    # Simulate
    try:
        maxsteps = int(sys.argv[1])
    except:
        maxsteps = 300
    for i in range(0,maxsteps):
        cellular.step([cstat, astat, fstat])
    fstat.save()
    # Plot map
    plotter = renderer.CellularMap(cstat.log)
    fig = plotter.plot()
    fig.show()
    # Plot metrics
    metrics = renderer.AgentMetrics(astat.log)
    fig = metrics.plot()
    fig.show()

if __name__ == "__main__":
    main()