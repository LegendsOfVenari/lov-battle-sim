from .venari import Venari
from effect import Web, Armor, Silence
from config import DamageType


class Eurici(Venari):

    def use_ability(self, target):
        super().use_ability(target)
        self.deal_damage(target, 15, DamageType.AP, 100)
        # web all enemies
        for enemy in self.battle.get_enemy_team(self):
            enemy.apply_effect(Web(self.messages, 3))

        self.apply_effect(Armor(self.messages))
        self.apply_effect(Armor(self.messages))

        self.messages.append(f"{self.name} used its ability!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.deal_damage(enemy_team[0], 10, DamageType.AP, 100)
        enemy_team[0].apply_effect(Silence(self.messages, 2))

        if enemy_team[0].has_effect_id("poison") or enemy_team[0].has_effect_id("web"):
            self.gain_energy(8)
            self.messages.append(f"{self.name} gained 8 energy from the enemy's poison/web!")
