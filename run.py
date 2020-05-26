import sys
import os

def _global_path(relative):
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, relative)
    return os.path.abspath(path)

sys.path.insert(0, _global_path('.'))

import automata

automata.main()
