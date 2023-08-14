import random
from .venari import Venari
from effect import Poison, Stagger, GuaranteedPoison
from .battle_utils import calculate_basic_attack_damage, calculate_ability_damage, DamageType

class Aharas(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)
        # Check if the Venari is staggered using a lambda function
        is_staggered = any(isinstance(effect, Stagger) for effect in self.active_effects)
        if is_staggered:
            print(f"{self.name}({self.level} got staggered!)")
        else:
            damage = calculate_basic_attack_damage(self, target, 35)
            target.hp -= damage

            # Generic
            self.energy += self.base_stats["Basic Attack Energy Gain"]
            self.energy = min(self.energy, 100)

            print(f"{self.name}({self.level}) attacked {target.name}({target.level}) for {damage:.2f} damage!")
            
            # Regular chance for Aharas to poison the target
            if random.random() < 0.2:
                target.apply_effect(Poison())
                print(f"{self.name}({self.level})'s poison triggered!")

    def use_ability(self, target):
        super().use_ability(target)
        if self.energy >= 100:
            # Remove all poison stacks from the target and deal bonus damage
            poison_stacks = len([effect for effect in target.active_effects if isinstance(effect, Poison)])
            damage = self.ability_power + (50 * poison_stacks)
            damage = calculate_ability_damage(DamageType.AD, self, target, 20 + 50 * poison_stacks)

            target.hp -= damage

            # Remove poison effects
            target.active_effects = [effect for effect in target.active_effects if not isinstance(effect, Poison)]

            print(f"{self.name} used its ability on {target.name},consuming {poison_stacks} and dealing {damage:.2f} damage!")
            self.energy -= 100

    def on_swap_in(self, enemy_team=None):
        """When Aharas is swapped in, its next basic attack applies poison."""
        super().on_swap_in()  # Call the base class's method to reset the attack tick counter
        self.apply_effect(GuaranteedPoison())
