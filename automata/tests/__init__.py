"""
Automata unit tests runner.

Imports: unittest
"""
from unittest import main
from . import __context

from automata.tests.test_core import *
from automata.tests.test_utils import *

if __name__ == "__main__":
    main()
