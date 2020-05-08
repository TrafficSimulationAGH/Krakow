from unittest import TestCase
import automata.utils as utils

class TExample(TestCase):
    def test_example(self):
        utils.example(2, 3, [])
        self.assertFalse(False)
