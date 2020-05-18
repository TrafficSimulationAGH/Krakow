"""
Mock data for unit tests.
"""
from automata.core import Cell

class MockStraightRoad:
    def __init__(self):
        self.start = Cell(None)
        self.start.add(Cell(None))
        self.start.add(Cell(None))
