from .venari import Venari
from effect import Unique, AccuracyDebuff
from config import DamageType


class Meeka(Venari):
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
        target.apply_effect(AccuracyDebuff(self.messages, 6, 50))

        self.messages.append(f"{self.name} used its ability on {target.name}!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.deal_damage(enemy_team[0], 20, DamageType.AD, 100)

    def get_opportunist_effect(self):
        return Unique(self.messages, "Opportunist", 2, 2)
