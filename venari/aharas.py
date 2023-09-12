from .venari import Venari
from effect import Poison
from config import DamageType


class Aharas(Venari):
    def apply_poison_effect(self, target):
        """Apply the Poison effect to the target."""
        target.apply_effect(Poison(self.messages, self.level, self.battle_stats.ability_power))

        self.messages.append(f"{self.name}({self.level})'s poison triggered!")

    def on_basic_attack_hit(self, target):
        """Override the base method to potentially apply a Poison effect on basic attack hit."""
        super().on_basic_attack_hit(target)
        poison_effect = target.get_effect("poison")
        if poison_effect is not None:
            poison_effect.reset_duration()
            self.messages.append(f"{self.name}({self.level})'s poison duration refreshed!")

    def use_ability(self, target):
        """Override the base method to deal additional damage based on the number of Poison stacks."""
        super().use_ability(target)

        # Calculate bonus damage based on poison stacks
        poison_effect = target.get_effect("poison")
        if poison_effect is not None:
            total_damage = poison_effect.calculate_total_remaining_damage(self) * 3
            self.deal_damage(target, total_damage, DamageType.AP, 100)

            # Remove poison effects
            target.remove_effect_id("poison")
            self.messages.append(f"{self.name} used its ability on {target.name}, dealing {total_damage} poison stacks.")
        else:
            self.apply_poison_effect(target)

    def on_swap_in(self, enemy_team=None):
        """Apply 1 stack of [Poison] to Point Venari."""
        super().on_swap_in()
        self.apply_poison_effect(enemy_team[0])

    def tick(self, is_point=True):
        """Override the base tick method."""
        super().tick(is_point)
