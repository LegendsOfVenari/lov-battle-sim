import random
from .venari import Venari
from effect import Poison, GuaranteedPoison
from config import DamageType


class Aharas(Venari):
    def apply_poison_effect(self, target):
        """Apply the Poison effect to the target."""
        target.apply_effect(Poison(self.messages, 4))

    def on_basic_attack_hit(self, target):
        """Override the base method to potentially apply a Poison effect on basic attack hit."""
        super().on_basic_attack_hit(target)

        if self.battle_handler.has_effect(GuaranteedPoison):
            self.battle_handler.remove_effect(GuaranteedPoison)
            self.apply_poison_effect(target)
        elif random.random() < 0.2:
            self.apply_poison_effect(target)
            self.messages.append(f"{self.name}({self.level})'s poison triggered!")

    def use_ability(self, target):
        """Override the base method to deal additional damage based on the number of Poison stacks."""
        super().use_ability(target)

        # Calculate bonus damage based on poison stacks
        poison_stacks = target.battle_handler.count_effects(Poison)
        bonus_damage = 20 + 50 * poison_stacks
        self.deal_damage(target, bonus_damage, DamageType.AP)

        # Remove poison effects
        target.battle_handler.remove_all_effects(Poison)

        self.messages.append(f"{self.name} used its ability on {target.name}, consuming {poison_stacks} poison stacks.")

    def on_swap_in(self, messages, enemy_team=None):
        """Apply the GuaranteedPoison effect when Aharas is swapped in."""
        super().on_swap_in(messages)

        if not self.battle_handler.has_effect(GuaranteedPoison):
            self.apply_effect(GuaranteedPoison(messages))

    def tick(self, is_point=True):
        """Override the base tick method."""
        super().tick(is_point)
