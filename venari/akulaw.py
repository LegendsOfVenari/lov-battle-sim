from .venari import Venari
import random
from effect import Stagger, DefenceDebuff, MagicResistDebuff
from .battle_utils import calculate_basic_attack_damage, calculate_ability_damage, DamageType

class Akulaw(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)

        # 20% chance of basic attacks applying stagger
        if random.random() < 0.2:
            target.apply_effect(Stagger())
            print(f"{self.name}({self.level})'s stagger triggered!")

    def use_ability(self, target):
        super().use_ability(target)
        damage = calculate_ability_damage(DamageType.AD, self, target, 66)
        target.receive_damage(damage)

        target.apply_effect(Stagger())
        print(f"{self.name} used its ability on {target.name}, dealing {damage:.2f} damage and staggering the target!")

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
        for enemy_venari in enemy_team:
            enemy_venari.apply_effect(DefenceDebuff())
            enemy_venari.apply_effect(MagicResistDebuff())

        print(f"{self.name}({self.level}) applied Defence and Magic Resist debuffs to the entire enemy team!")
