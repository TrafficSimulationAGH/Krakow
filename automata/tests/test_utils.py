from unittest import TestCase
import automata.utils as utils

class TExample(TestCase):
    def test_example(self):
        r = utils.example(2, [])
        self.assertEqual(r, 0)
