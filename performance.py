import sys
import os

def _global_path(relative):
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, relative)
    return os.path.abspath(path)

sys.path.insert(0, _global_path('.'))

import automata
import time
import numpy as np

times = []
steps = np.geomspace(1e-5, 1e-3, num=20)
#steps = [20*x for x in range(1,21)]
for i in steps:
    automata.utils.CONFIG.RADIUS = i
    start = time.time()
    automata.simulate(100)
    end = time.time()
    times.append(end - start)
    print("{0} - time {1}".format(i, times[-1]))

print(list(zip(steps, times)))

