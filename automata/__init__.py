"""
Automata - a traffic simulation package.
Imports: numpy, matplotlib
"""
from . import renderer
from . import core
from . import utils

def main():
    data = core.OSM('krakow.json')
    m = renderer.Plotter(data, lambda frame: None)
    m.plot()
    ff = data.filter(lambda i: 'toll' in i['properties'])
    utils.plot_elements(ff, clr='r', ax=m.ax)
    m.show()

if __name__ == "__main__":
    main()