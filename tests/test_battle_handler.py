import unittest
from unittest.mock import Mock
from venari import BattleHandler, Venari
from battle import Battle
from config import DamageType, laticus_base_stats

class TestBattleHandler(unittest.TestCase):
    def setUp(self):
        self.battle_handler = BattleHandler([])
        self.mock_venari = Venari("Test Venari", laticus_base_stats, 1, {}, True)

        # Mock battle
        self.mock_battle = Battle(self, [selmock_venari], team2, tick_count, messages, team1_arena_effects=None, team2_arena_effects=None):

    def test_gain_energy(self):
        self.battle_handler.gain_energy(10)
        self.assertEqual(self.battle_handler.energy, 10)

    def test_basic_attack(self):
        self.mock_venari.battle_stats.accuracy = 100
        self.mock_venari.battle_stats.dodge_chance = 0
        self.battle_handler.basic_attack(self.mock_venari, self.mock_venari)
        self.assertEqual(self.battle_handler.attack_tick_counter, 0)

    def test_deal_damage(self):
        self.mock_venari.battle_stats.accuracy = 100
        self.mock_venari.battle_stats.dodge_chance = 0
        self.battle_handler.deal_damage(self.mock_venari, self.mock_venari, 10, DamageType.AD, 100)
        self.assertIn("Dealt", self.battle_handler.messages[-1])

    def test_receive_damage(self):
        self.mock_venari.battle_stats.hp = 100
        self.battle_handler.receive_damage(self.mock_venari, 10)
        self.assertEqual(self.mock_venari.battle_stats.hp, 90)

    def test_apply_effect(self):
        mock_effect = Mock()
        mock_effect.effect_id = "test_effect"
        self.battle_handler.apply_effect(mock_effect, self.mock_venari)
        self.assertIn("test_effect", self.battle_handler.active_effects)

    # Add more tests...

if __name__ == '__main__':
    unittest.main()