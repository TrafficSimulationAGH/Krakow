import sys
import os

def _global_path(relative):
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, relative)
    return os.path.abspath(path)

sys.path.insert(0, _global_path('.'))

import automata
import time

times = []
steps = [20 * x for x in range(1,50)]
for i in steps:
    start = time.time()
    automata.main(i)
    end = time.time()
    times.append(end - start)

print(list(zip(steps, times)))
