"""
Core definitions, basic structures.
"""
import automata.utils
import automata.simplemap
import automata.stats
from random import random
import math
import numpy as np

class Vehicle:
    """
    Static variables:
    V_MAX - maximum speed (km/h)
    SLOW - probability of braking
    FAST - probability of accelerating
    LIMIT - probability of matching with speed limit
    """
    V_MAX = automata.utils.CONFIG.AGENT_VMAX
    DRIVEOFF = automata.utils.CONFIG.AGENT_DRIVEOFF
    SLOW = automata.utils.CONFIG.AGENT_SLOW
    FAST = automata.utils.CONFIG.AGENT_FAST
    LIMIT = automata.utils.CONFIG.AGENT_LIMIT

    def __init__(self, v):
        self.v = v
        self.cell = None

    def is_off(self):
        "Check whether agent got off map"
        return self.cell is None

    def randomize(self):
        "Change variables randomly"
        vmax = automata.utils.speed2vcell(self.V_MAX)
        if self.v > 1 and random() < self.SLOW:
            self.v -= 1
        elif self.v < vmax and random() < self.FAST:
            self.v += 1
        elif random() < self.LIMIT:
            self.v = min(self.cell.speed_lim, vmax)

    def step(self):
        "Move forward"
        self.randomize()
        n = self.v
        while n > 0:
            n -= 1
            if self.cell.is_connected() and self.cell.forward.is_free():
                self.cell.set_vehicle(None)
                # Next cell is SpawnPoint if a new road starts
                if type(self.cell.forward) is SpawnPoint and random() < self.DRIVEOFF:
                    break
                self.cell.forward.set_vehicle(self)

class Cell:
    """
    Road cell containing information about:
    - lanes
    - speed limit
    - coordinates
    - vehicles inside
    - adjacent cells - forward
    """
    TYPE = 'Cell'

    def __init__(self, coords, lanes=1, speed_lim=140.0):
        self.id = 0
        self.lanes = lanes
        self.speed_lim = automata.utils.speed2vcell(speed_lim)
        self.coords = np.array(coords)
        self.forward = None
        self.vehicles = 0

    def __eq__(self, other):
        if other is None:
            return False
        return (self.coords == other.coords).all()

    def __repr__(self):
        return '<{0} {1} free:{2}>'.format(self.TYPE, self.coords, self.is_free())

    def is_connected(self):
        "Checks if forward cell is set"
        return self.forward is not None

    def is_free(self):
        "Checks whether cell can accept another vehicle"
        return self.vehicles < self.lanes

    def append(self, cell):
        "Set adjacent cell on first None adjacent pointer"
        if self.forward is None:
            self.forward = cell
        else:
            self.forward.append(cell)

    def set_vehicle(self, vehicle):
        "Set pointers for cell and vehicle. None reduces counter."
        if vehicle is not None:
            self.vehicles += 1
            vehicle.cell = self
        else:
            if self.vehicles > 0:
                self.vehicles -= 1

    def copy(self):
        cell = Cell(self.coords, self.lanes, self.speed_lim)
        cell.forward = self.forward
        cell.turn = self.turn
        cell.__class__ = self.__class__
        return cell

    @staticmethod
    def from_point(point):
        point.__class__ = Cell
        return point

class EndPoint(Cell):
    """
    Cell derived class that removes all vehicles that enter it.
    """
    TYPE = 'EndPoint'

    @staticmethod
    def from_cell(cell: Cell):
        cell.__class__ = EndPoint
        return cell

class SpawnPoint(Cell):
    """
    Cell derived class that populates itself with vehicles.
    Loads config SPAWN_RATE as default RATE.
    RATE - probability of spawning
    """
    TYPE = 'SpawnPoint'
    RATE = automata.utils.CONFIG.SPAWN_RATE

    def spawn(self):
        "Spawn a vehicle with a random chance. Returns spawned object."
        if self.is_free() and random() < self.RATE:
            vh = Vehicle(self.speed_lim)
            self.set_vehicle(vh)
            return vh
        return None

    @staticmethod
    def from_cell(cell: Cell):
        cell.__class__ = SpawnPoint
        return cell

class Cellular:
    """
    Simulation runner class.
    List of cells, list of agents and list of spawns.
    Loads config: RADIUS.
    """

    def __init__(self):
        self.iteration = 0
        self.agents = []
        self.array = []
        self.spawns = []
        self.stat = automata.stats.Stat()

    def step(self):
        "Perform simulation step. Call spawners and agents."
        self.iteration += 1
        # Clear agents that do not exist on map
        self.agents = [x for x in self.agents if not x.is_off()]
        # Simulate car movement
        for x in self.agents:
            if x is None:
                continue
            x.step()
        # Traffic enters road
        for x in self.spawns:
            v = x.spawn()
            if v is not None:
                self.agents.append(v)
        # Log
        if self.stat is not None:
            self.stat.append(self)

    def offset_lane(self, line, n):
        "Cells coordinates moved perpendicularly to create a new lane"
        n += 5 * n / abs(n)
        # Estimate heading between first and last cell
        vec = line[-1] - line[0]
        heading = math.atan2(vec[1], vec[0]) + math.pi / 2
        # Offset vector
        vec = np.array([math.cos(heading), math.sin(heading)]) * automata.utils.CONFIG.RADIUS * n
        coords = line + np.ones(line.shape) * vec
        return coords
    
    def cells_fill(self, line, lanes=1):
        "Evenly distribute cells along line coordinates"
        reg = []
        dec = 1
        for i in range(1,len(line)):
            vec = np.array(line[i]) - np.array(line[i-dec])
            n = int(round(np.linalg.norm(vec) / automata.utils.CONFIG.RADIUS))
            if n <= 0:
                # Cells are too close - try extending range
                dec += 1
            else:
                intercells = np.linspace(line[i-dec], line[i], num=n, endpoint=False)
                reg += [Cell(coords, lanes) for coords in intercells]
                dec = 1
        for i in range(1,len(reg)):
            reg[i-1].append(reg[i])
        return reg

    def reindex(self):
        "Reindex array elements with id"
        for i in range(0,len(self.array)):
            self.array[i].id = i

    def resolve_destination(self, cells_dict):
        "Connect cells that match start with destination"
        directions = list(cells_dict.keys())
        for k in directions:
            match = None
            for x in directions:
                if x[0] == k[1]:
                    match = x
                    break
            if match is not None:
                cells_dict[k][-1].append(cells_dict[match][0])
        return cells_dict

    def build(self, data:automata.simplemap.SM):
        "Construct cellular grid from SM object"
        clockwise = {}
        anticlock = {}
        for road in data.roads:
            # Clockwise road
            r = road.clockwise()
            offset = self.offset_lane(r.points, 1)
            cw = self.cells_fill(offset, lanes=r.lanes)
            cw[0] = SpawnPoint.from_cell(cw[0])
            cw[-1] = EndPoint.from_cell(cw[-1])
            clockwise.update({r.destination: cw})
            # Anticlockwise road
            r = road.anticlockwise()
            acw = self.cells_fill(r.points, lanes=r.lanes)
            acw[0] = SpawnPoint.from_cell(acw[0])
            acw[-1] = EndPoint.from_cell(acw[-1])
            anticlock.update({r.destination: acw})
        # Connect roads basing on destination
        clockwise = self.resolve_destination(clockwise)
        anticlock = self.resolve_destination(anticlock)
        # To array
        self.array = []
        for k in clockwise:
            self.array += clockwise[k]
        for k in anticlock:
            self.array += anticlock[k]
        # Hurray, retrieve spawnpoints and reindex array
        self.spawns = [x for x in self.array if type(x) is SpawnPoint]
        self.reindex()
        