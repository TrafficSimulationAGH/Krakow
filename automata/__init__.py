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
    m.show()

if __name__ == "__main__":
    main()