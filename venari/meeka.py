from .venari import Venari
from effect import Unique, Bleed
from config import DamageType


class Meeka(Venari):
    def on_ally_basic_attack(self, attacker):
        if self.battle_handler.is_assist and attacker is not self:
            enemy_point_venari = self.get_enemy_point_venari()
            super().basic_attack(enemy_point_venari)

    def basic_attack(self, target):
        if target.has_effect_id("bleed"):
            super().basic_attack(target, 20)
            self.messages.append(f"{self.name} dealt an empowered auto attack.")
        else:
            super().basic_attack(target)

    def use_ability(self, target):
        super().use_ability(target)
        target.apply_effect(Bleed(self.messages, self.level, self.battle_stats.attack_damage, 6, 6))

        self.messages.append(f"{self.name} used its ability on {target.name}!")
