"""
This module serves the package basing on its path.
"""
import sys
import os

def _global_path():
    folder = os.path.dirname(__file__)
    upupdir = os.path.join('..','..')
    path = os.path.join(folder, upupdir)
    return os.path.abspath(path)

sys.path.insert(0, _global_path())
