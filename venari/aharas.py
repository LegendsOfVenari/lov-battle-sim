import random
from .venari import Venari
from effect import Poison, GuaranteedPoison
from .battle_utils import calculate_ability_damage, DamageType


class Aharas(Venari):
    def __init(self, name, base_stats, level):
        self.poison_applied = False

    def basic_attack(self, target, messages):
        super().basic_attack(target, messages)

        # 20% chance of basic attacks applying poison
        if not self.poison_applied and random.random() < 0.2:
            target.apply_effect(Poison(), messages)
            self.poison_applied = True
            messages.append(f"{self.name}({self.level})'s poison triggered!")

    def use_ability(self, target, messages):
        super().use_ability(target)
        # Remove all poison stacks from the target and deal bonus damage
        poison_stacks = len([effect for effect in target.active_effects if isinstance(effect, Poison)])
        damage = calculate_ability_damage(DamageType.AP, self, target, 20 + 50 * poison_stacks)
        target.receive_damage(damage)

        # Remove poison effects
        target.active_effects = [effect for effect in target.active_effects if not isinstance(effect, Poison)]

        messages.append(f"{self.name} used its ability on {target.name},consuming {poison_stacks} and dealing {damage:.2f} damage!")

    def on_swap_in(self, messages, enemy_team=None):
        """When Aharas is swapped in, its next basic attack applies poison."""
        super().on_swap_in(messages)  # Call the base class's method to reset the attack tick counter
        self.apply_effect(GuaranteedPoison(), messages)

    def reset_action(self):
        super().reset_action()  # Call the base class's reset_action method to reset the action_performed flag
        self.poison_applied = False
