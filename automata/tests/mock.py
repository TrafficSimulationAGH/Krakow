"""
Mock data for unit tests.
"""
import os.path
import numpy as np
from automata.core import Cell, Cellular

def tests_path(path):
    if os.path.exists(path):
        return path
    else:
        return f"automata/tests/{path}"

MockCellularMap = Cellular()

MockStraightRoad = Cell([])
MockStraightRoad.add(Cell([]))
MockStraightRoad.add(Cell([]))
