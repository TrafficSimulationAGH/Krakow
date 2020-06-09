"""
Statistics logging module.
"""
import pandas as pd
import automata.utils

class Stat:
    "Statistics abstract class for logging."

    def __init__(self):
        self.cell_log = None
        self.agent_log = None

    def save(self, fpath='log.csv'):
        """
        Save logs to files:
        cell.fpath - cellular log
        agent.fpath - agents log
        """
        if self.cell_log is not None:
            self.cell_log.to_csv(f'cell.{fpath}', sep=';')
        if self.agent_log is not None:
            self.agent_log.to_csv(f'agent.{fpath}', sep=';')

    def log_cells(self, cell_array, it):
        "Log cells state."
        update = [cell2dict(x, it) for x in cell_array]
        if len(update) > 0:
            if self.cell_log is None:
                self.cell_log = pd.DataFrame(update)
            else:
                self.cell_log = self.cell_log.append(update, ignore_index=True)

    def log_agents(self, agent_array, it):
        "Log agents state."
        update = [agent2dict(x, it) for x in agent_array]
        if len(update) > 0:
            if self.agent_log is None:
                self.agent_log = pd.DataFrame(update)
            else:
                self.agent_log = self.agent_log.append(update, ignore_index=True)

    def append(self, cellular):
        "Append logs row to DataFrames."
        self.log_cells(cellular.array, cellular.iteration)
        self.log_agents(cellular.agents, cellular.iteration)

def cell2dict(cell, iteration=0):
    return {
        'x': cell.coords[0],
        'y': cell.coords[1],
        'id': cell.id,
        'lanes': cell.lanes,
        'density': round(cell.vehicles / cell.lanes, 2),
        'speed_lim': cell.speed_lim,
        'type': cell.TYPE,
        'iteration': iteration
    }

def agent2dict(agent, iteration=0):
    return {
        'id': agent.cell.id,
        'v': agent.v,
        'km/h': automata.utils.vcell2speed(agent.v),
        'iteration': iteration
    }
