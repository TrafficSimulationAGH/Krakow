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
        return [{'iteration': cellular.iteration}]

    def append(self, cellular):
        "Append logs row to DataFrames."
        update = self.extract(cellular)
        if len(update) > 0:
            if self.log is None:
                if type(update) is pd.DataFrame:
                    self.log = update
                else:
                    self.log = pd.DataFrame(update)
            else:
                if type(update) is pd.DataFrame:
                    self.log = pd.concat([self.log, update], ignore_index=True, copy=False)
                else:
                    self.log = pd.concat([self.log, pd.DataFrame(update)], ignore_index=True, copy=False)

class InOutFlowStat(Stat):
    "Log in and out flow events."

    def extract(self, cellular):
        agent_out = [x for x in cellular.agents if x.is_off]
        agent_in = [x for x in cellular.agents if x.lifetime < 1]
        data = []
        for x in agent_out:
            data.append({'iteration':cellular.iteration, 'type':'out', 'crossing':x.cell.destination[1], 'lifetime':x.lifetime, 'flow':1})
        for x in agent_in:
            data.append({'iteration':cellular.iteration, 'type':'in', 'crossing':x.cell.destination[0], 'lifetime':x.lifetime, 'flow':1})
        sumdf = pd.DataFrame(data).groupby(['iteration','type','crossing']).sum()
        return sumdf.reset_index()

class CellStat(Stat):
    "Log Cell state into a dataframe."

    def extract(self, cellular):
        return [cell2dict(x, cellular.iteration) for x in cellular.array]

class LastCellStat(CellStat):
    "Logger discarding historical changes. For performance boosting."

    def __init__(self, filename='log.csv', size=50):
        super().__init__(filename)
        self._stored = 0
        self.size = size

    def append(self, cellular):
        "Append logs row to DataFrames. Discard previous state."
        update = self.extract(cellular)
        if len(update) > 0:
            if self._stored < 1:
                self._stored = 1
                self.log = pd.DataFrame(update)
            elif self._stored < self.size:
                self._stored += 1
                self.log = pd.concat([self.log, pd.DataFrame(update)], ignore_index=True, copy=False)
            else:
                m = self.log['iteration'].min()
                m = self.log[self.log['iteration'] == m].index
                self.log = self.log.drop(m)
                self.log = pd.concat([self.log, pd.DataFrame(update)], ignore_index=True, copy=False)

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
        'density': round(cell.vehicles / max(cell.lanes,1), 2),
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
        'is_off': agent.is_off,
        'lifetime': agent.lifetime,
        'iteration': iteration
    }
