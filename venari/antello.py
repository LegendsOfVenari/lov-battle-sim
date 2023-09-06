from .venari import Venari
from effect import NourishingResilience, MoonlightVigor
from arena_effect import GracefulEmbraceAura


class Antello(Venari):
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
        if 'nourishing_resilience' not in self.battle_handler.active_effects:
            self.apply_effect(NourishingResilience(self.messages))

    def on_basic_attack_hit(self, target):
        super().on_basic_attack_hit(target)

    def use_ability(self, target):
        super().use_ability(target)
        self.battle.add_ally_arena_effect(GracefulEmbraceAura(self.messages, 12), self)

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()

        heal_amount = self.battle_stats.initial_hp * 0.3
        self.apply_effect(MoonlightVigor(self.messages, heal_amount))
