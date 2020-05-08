"""
This module serves the package basing on its path.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.join('..','..'))))
