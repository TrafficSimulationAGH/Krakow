"""
Mock data for unit tests.
"""
import numpy as np
from automata.openmap import OSM
from automata.core import Cell, Cellular

# TODO: build full net
def npy2cells():
    npy = np.load('mock.npy', allow_pickle=True)
    cells = []
    for x in npy:
        if type(x[1]['coordinates'][0]) is float:
            cells.append(Cell(x[1]['coordinates'], info=x[0]))
        else:
            cells += [Cell(c, info=x[0]) for c in x[1]['coordinates']]
      
    return cells

MockCellularMap = Cellular()
MockCellularMap.array = npy2cells()

MockJsonMap = OSM('mock.json')

MockStraightRoad = Cell(None)
MockStraightRoad.add(Cell(None))
MockStraightRoad.add(Cell(None))
