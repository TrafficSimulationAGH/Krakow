"""
Statistics logging module.
"""
import pandas as pd
import automata.utils

class Stat:
    "Statistics abstract class for logging."

    def __init__(self, filename='log.csv'):
        self.filename = filename
        self.log = None

    def load(self, fpath):
        "Load log from specified path."
        self.log = pd.read_csv(fpath, sep=';')

    def save(self):
        "Save log to file in append mode."
        if self.log is not None:
            self.log.to_csv(self.filename, sep=';', index=False, mode='a')

    def extract(self, cellular):
        "Construct list of dicts from given state"
        return [{'id': x.id, 'vehicles': x.vehicles, 'iteration': cellular.iteration} for x in cellular.array]

    def append(self, cellular):
        "Append logs row to DataFrames."
        update = self.extract(cellular)
        if len(update) > 0:
            if self.log is None:
                self.log = pd.DataFrame(update)
            else:
                self.log = self.log.append(update, ignore_index=True)

class InOutFlowStat(Stat):
    "Log in and out flow events."

    def extract(self, cellular):
        return super().extract(cellular)

class CellStat(Stat):
    "Log Cell state into a dataframe."

    def extract(self, cellular):
        return [cell2dict(x, cellular.iteration) for x in cellular.array]

class LastCellStat(CellStat):
    "Logger discarding historical changes. For performance boosting."

    def __init__(self, filename='log.csv', size=50):
        self._stored = 0
        self.filename = filename
        self.size = size
        self.log = None

    def append(self, cellular):
        "Append logs row to DataFrames. Discard previous state."
        update = self.extract(cellular)
        if len(update) > 0:
            if self._stored < 1:
                self._stored = 1
                self.log = pd.DataFrame(update)
            elif self._stored < self.size:
                self._stored += 1
                self.log = self.log.append(update, ignore_index=True)
            else:
                m = self.log['iteration'].min()
                m = self.log[self.log['iteration'] == m].index
                self.log = self.log.drop(m)
                self.log = self.log.append(update, ignore_index=True)

class AgentStat(Stat):
    "Log agent state into a dataframe."

    def extract(self, cellular):
        return [agent2dict(x, cellular.iteration) for x in cellular.agents]

def cell2dict(cell, iteration=0):
    return {
        'x': cell.coords[0],
        'y': cell.coords[1],
        'id': cell.id,
        'lanes': cell.lanes,
        'density': round(cell.vehicles / cell.lanes, 2),
        'speed_lim': cell.speed_lim,
        'type': cell.TYPE,
        'destination': cell.destination,
        'iteration': iteration
    }

def agent2dict(agent, iteration=0):
    return {
        'id': agent.cell.id,
        'v': agent.travelled,
        'km/h': automata.utils.vcell2speed(agent.travelled),
        'iteration': iteration
    }
