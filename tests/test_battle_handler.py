import unittest
from venari import BattleHandler

class TestBattleHandler(unittest.TestCase):
    def setUp(self):
        self.battle_handler = BattleHandler([])

    def test_gain_energy(self):
        self.battle_handler.gain_energy(10)
        self.assertEqual(self.battle_handler.energy, 10)

    # Add more tests...

if __name__ == '__main__':
    unittest.main()