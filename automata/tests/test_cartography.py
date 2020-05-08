from unittest import TestCase
import automata.cartography as cart

class TLane(TestCase):
    def test_init(self):
        a = cart.Lane()
        self.assertIsNotNone(a)
