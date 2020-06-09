"""
Automata - a traffic simulation package.
Imports: numpy, matplotlib
"""
from . import config
from . import core
from . import utils
from . import stats
from . import renderer
from . import simplemap
from . import openmap

def main():
    utils.CONFIG.RADIUS = 1e-4
    sm = simplemap.SM('krakow.json')
    cellular = core.Cellular()
    cellular.build(sm)
    cstat = stats.CellStat()
    astat = stats.AgentStat('agent.log')
    for i in range(0,100):
        cellular.step([cstat, astat])
    log = cstat.log[cstat.log['iteration'] > 90]
    plotter = renderer.CellularPlotter(log)
    fig = plotter.plot()
    fig.show()

if __name__ == "__main__":
    main()