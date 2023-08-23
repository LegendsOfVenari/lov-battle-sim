from .venari import Venari
from effect import Unique, AccuracyDebuff
from config import DamageType


class Nyrie(Venari):
    def basic_attack(self, target):
        effect = self.get_opportunist_effect()
        if self.battle_handler.has_effect(effect):
            self.battle_handler.remove_effect(effect, self)
            super().basic_attack(target, 30)
            self.messages.append(f"{self.name} dealt an empowered auto attack.")
        else:
            super().basic_attack(target)

    def on_target_miss(self, target):
        super().on_target_miss(target)
        self.apply_effect(Unique(self.messages, "opportunist", 5, 5))
        self.messages.append(f"{self.name}({self.level})'s gained an opportunist stack!")

    def use_ability(self, target):
        super().use_ability(target)

        # Calculate the damage based on Algala's Attack Damage (AD)
        if target.battle_stats.hp_percentage() >= 0.75:
            self.deal_damage(target, 110, DamageType.AD, 100)
        else:
            self.deal_damage(target, 60, DamageType.AD, 100)

        self.messages.append(f"{self.name} used its ability on {target.name}!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        enemy_team[0].apply_effect(AccuracyDebuff(self.messages, 12, 50))

    def get_opportunist_effect(self):
        return Unique(self.messages, "Natural Touch", 6, 6)