from .venari import Venari
import random
from effect import Stagger, DefenceDebuff, MagicResistDebuff

class Akulaw(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)
    
        damage = self.attack_damage
        target.hp -= damage

        # Energy gain from basic attack
        self.energy += self.base_stats["Basic Attack Energy Gain"]
        self.energy = min(self.energy, 100)

        print(f"{self.name}({self.level}) attacked {target.name}({target.level}) for {damage:.2f} damage!")
    
        # 20% chance of basic attacks applying stagger
        if random.random() < 0.2:
            target.apply_effect(Stagger())
            print(f"{self.name}({self.level})'s stagger triggered!")

    def use_ability(self, target):
        super().use_ability(target)
        if self.energy >= 100:
            damage = self.attack_damage
            target.hp -= damage
            target.apply_effect(Stagger())
            print(f"{self.name} used its ability on {target.name}, dealing {damage:.2f} damage and staggering the target!")
            self.energy -= 100

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
        for enemy_venari in enemy_team:
            enemy_venari.apply_effect(DefenceDebuff())
            enemy_venari.apply_effect(MagicResistDebuff())

        print(f"{self.name}({self.level}) applied Defence and Magic Resist debuffs to the entire enemy team!")
