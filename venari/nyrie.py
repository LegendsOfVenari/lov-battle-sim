from .venari import Venari
from effect import NaturalTouch, Shield
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
            effect = NaturalTouch(self.messages)
            self.apply_effect(effect)
            effect.reset()

    def basic_attack(self, target):
        super().basic_attack(target)
        self.apply_effect(NaturalTouch(self.messages))

    def use_ability(self, target):
        super().use_ability(target)
        ally_team = self.battle.get_ally_team(self)
        if ally_team:
            for venari in ally_team:
                shield_amount = venari.battle_handler.calculate_ability_power(self.level, self.battle_stats.ability_power, 60)
                venari.apply_effect(Shield(self.messages, shield_amount, 6))

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        ally_bench = self.get_ally_bench()
        for venari in ally_bench:
            if venari is not self:
                venari.reduce_swap_cooldown(1)

        ally_point_venari = self.get_ally_point_venari()
        shield_amount = self.battle_handler.calculate_ability_power(self.level, self.battle_stats.ability_power, 20)
        ally_point_venari.apply_effect(Shield(self.messages, shield_amount, 6))
