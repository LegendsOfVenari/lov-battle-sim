from .venari import Venari
from effect import Unique, AccuracyDebuff, NaturalTouch
from config import DamageType


class Nyrie(Venari):
    def __init__(self,
                 name,
                 base_stats,
                 level,
                 messages,
                 isPlayerVenari,
                 battle=None,
                 battle_handler=None,
                 battle_stats=None):
        super().__init__(name,
                         base_stats,
                         level,
                         messages,
                         isPlayerVenari,
                         battle,
                         battle_handler,
                         battle_stats)
        if 'natural_touch' not in self.battle_handler.active_effects:
            self.apply_effect(NaturalTouch(self.messages))

    def basic_attack(self, target):
        super().basic_attack(target)
        self.apply_effect(NaturalTouch(self.messages))

    def use_ability(self, target):
        super().use_ability(target)

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        ally_bench = self.get_ally_bench()
        for venari in ally_bench:
            venari.reduce_swap_cooldown(2)
