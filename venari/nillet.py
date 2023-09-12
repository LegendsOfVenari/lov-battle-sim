from .venari import Venari
from effect import Stagger, HaresAcceleration
from config import DamageType

class Nillet(Venari):
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
        if 'hares_acceleration' not in self.battle_handler.active_effects:
            effect = HaresAcceleration(self.messages)
            self.apply_effect(effect)
            effect.reset()

    def use_ability(self, target):
        super().use_ability(target)
        target.apply_effect(Stagger(self.messages))
        self.battle_handler.attack_tick_counter = 100

        hares_acceleration = self.get_effect("hares_acceleration")
        hares_acceleration.stack(self)

        self.messages.append(f"{self.name} used its ability, staggering the enemy and resetting its attack counter!")

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
        ally_point_venari = self.get_ally_point_venari()
        ally_point_venari.attack_tick_counter = 100

    def on_swap_out(self):
        hares_acceleration = self.get_effect("hares_acceleration")
        hares_acceleration.reset()
        return super().on_swap_out()
