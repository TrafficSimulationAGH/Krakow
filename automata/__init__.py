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
    sm = simplemap.SM('krakow.json')
    cellular = core.Cellular()
    cellular.build(sm)
    for i in range(0,200):
        cellular.step()
    log = cellular.stat.cell_log
    log = log[log['iteration'] > 190]
    plotter = renderer.CellularPlotter(log)
    fig = plotter.plot()
    fig.show()

if __name__ == "__main__":
    main()