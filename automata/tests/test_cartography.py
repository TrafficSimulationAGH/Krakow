from unittest import TestCase
import automata.cartography as acg

class TLane(TestCase):
    def test_init(self):
        a = acg.Lane()
        self.assertIsNotNone(a)
