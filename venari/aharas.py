import random
from .venari import Venari
from effect import Poison, GuaranteedPoison
from config import DamageType


class Aharas(Venari):
    def basic_attack(self, target):
        did_damage = super().basic_attack(target)
        if did_damage:
            # 20% chance of basic attacks applying poison
            if self.battle_handler.find_effect(GuaranteedPoison) is not None:
                self.battle_handler.remove_active_effect(GuaranteedPoison)
                target.apply_effect(Poison(self.messages, 4))
            elif random.random() < 0.2:
                target.apply_effect(Poison(self.messages, 4))
                self.messages.append(f"{self.name}({self.level})'s poison triggered!")

    def use_ability(self, target):
        super().use_ability(target)
        # Remove all poison stacks from the target and deal bonus damage
        poison_stacks = len([effect for effect in target.battle_handler.active_effects if isinstance(effect, Poison)])
        self.deal_damage(target, 20 + 50 * poison_stacks, DamageType.AP)

        # Remove poison effects
        target.battle_handler.active_effects = [effect for effect in target.battle_handler.active_effects if not isinstance(effect, Poison)]

        self.messages.append(f"{self.name} used its ability on {target.name},consuming {poison_stacks}")

    def on_swap_in(self, messages, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in(messages)

        # When Aharas is swapped in, its next basic attack applies poison.
        self.apply_effect(GuaranteedPoison(messages))

    def tick(self, is_point=True):
        super().tick(is_point)
