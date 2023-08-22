import random
from .venari import Venari
from effect import Poison, DodgeBuff
from config import DamageType


class Aharas(Venari):
    def apply_poison_effect(self, target):
        """Apply the Poison effect to the target."""
        target.apply_effect(Poison(self.messages))

        self.messages.append(f"{self.name}({self.level})'s poison triggered!")

    def on_basic_attack_hit(self, target):
        """Override the base method to potentially apply a Poison effect on basic attack hit."""
        super().on_basic_attack_hit(target)
        self.apply_poison_effect(target)
        self.messages.append(f"{self.name}({self.level})'s poison triggered!")

    def use_ability(self, target):
        """Override the base method to deal additional damage based on the number of Poison stacks."""
        super().use_ability(target)

        # Calculate bonus damage based on poison stacks
        poison_stacks = target.battle_handler.count_stacks(Poison.get_id())
        print(poison_stacks)
        bonus_damage = 20 + 50 * poison_stacks
        self.deal_damage(target, bonus_damage, DamageType.AP)

        # Remove poison effects
        target.battle_handler.remove_effect(Poison.get_id())

        self.messages.append(f"{self.name} used its ability on {target.name}, consuming {poison_stacks} poison stacks.")

    def on_swap_in(self, enemy_team=None):
        """Apply a 50% dodge buff for 5 ticks when Aharas is swapped in."""
        super().on_swap_in()
        dodgeBuff = DodgeBuff(50, self.messages, 5)
        if not self.battle_handler.has_effect(dodgeBuff):
            self.apply_effect(dodgeBuff)

    def tick(self, is_point=True):
        """Override the base tick method."""
        super().tick(is_point)
