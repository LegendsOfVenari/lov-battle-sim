import unittest
from unittest.mock import MagicMock
from venari.venari import Venari

class TestVenari(unittest.TestCase):
    def setUp(self):
        self.base_stats = MagicMock()
        self.battle_stats = MagicMock()
        self.venari = Venari("Test", self.base_stats, 1, [], True, battle_stats=self.battle_stats)

if __name__ == '__main__':
    unittest.main()