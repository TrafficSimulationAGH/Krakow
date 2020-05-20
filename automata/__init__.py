"""
Automata - a traffic simulation package.

Imports: numpy, matplotlib
"""
import renderer
import core

def main():
    data = core.OSM('krakow.json')
    m = renderer.Plotter(data, lambda frame: None)
    m.plot()
    m.show()

if __name__ == "__main__":
    main()
