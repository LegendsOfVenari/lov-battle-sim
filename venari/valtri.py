from .venari import Venari
from effect import LoneSurvivor, MoonlitHuntMark, Bleed
from config import DamageType


class Valtri(Venari):
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
        if 'lone_survivor' not in self.battle_handler.active_effects:
            self.apply_effect(LoneSurvivor(self.messages))

    def use_ability(self, target):
        super().use_ability(target)
        enemy_team = self.battle.get_enemy_team(self)
        for venari in enemy_team:
            venari.apply_effect(MoonlitHuntMark(self.messages))

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.deal_damage(enemy_team[0], 10, DamageType.AD, 100)
        enemy_team[0].apply_effect(Bleed(self.messages, self.level, self.battle_stats.attack_damage))
