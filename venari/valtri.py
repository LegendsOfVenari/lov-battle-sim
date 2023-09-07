from .venari import Venari
from effect import AccuracyDebuff, MoonlitHuntMark, Bleed
from config import DamageType


class Valtri(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)
        # If valtri targets a marked enemy, reduce attack cooldown by 1
        if target.has_effect_id("moonlit_hunt_mark"):
            self.reduce_swap_cooldown(1)

    def use_ability(self, target):
        super().use_ability(target)
        enemy_team = self.battle.get_enemy_team(self)
        for venari in enemy_team:
            venari.apply_effect(MoonlitHuntMark(self.messages))

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.deal_damage(enemy_team[0], 10, DamageType.AD, 100)
        enemy_team[0].apply_effect(AccuracyDebuff(self.messages, 3, 50))
