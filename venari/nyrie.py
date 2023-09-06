from .venari import Venari
from effect import NaturalTouch
from arena_effect import ReadyToHelpAura


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
        heal_amount = self.battle_handler.calculate_ability_power(self, 30)
        self.battle.add_ally_arena_effect(ReadyToHelpAura(self.messages, 6, False, heal_amount), self)

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        ally_bench = self.get_ally_bench()
        for venari in ally_bench:
            venari.reduce_swap_cooldown(1)
