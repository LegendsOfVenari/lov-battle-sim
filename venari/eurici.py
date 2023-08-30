from .venari import Venari
from effect import Web, Armor, Guard
from config import DamageType


class Eurici(Venari):

    def use_ability(self, target):
        super().use_ability(target)
        self.deal_damage(target, 15, DamageType.AP, 100)
        # web all enemies
        for enemy in self.battle.get_enemy_team(self):
            enemy.apply_effect(Web(self.messages, 3))
            self.apply_effect(Armor(self.messages))

        self.messages.append(f"{self.name} used its ability!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()

        self.apply_effect(Guard(self.messages, 6))
