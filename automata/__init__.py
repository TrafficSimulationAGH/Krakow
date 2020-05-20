"""
Automata - a traffic simulation package.

Imports: numpy, matplotlib
"""
import renderer as renderer

def main():
    data = renderer.MapData('krakow.json')
    m = renderer.Plotter(data, lambda frame: None)
    m.blank()
    m.render()

if __name__ == "__main__":
    main()
