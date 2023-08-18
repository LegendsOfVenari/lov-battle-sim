from .venari import Venari
import random
from effect import Stagger, DefenceDebuff, MagicResistDebuff
from config import DamageType

class Akulaw(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)

    def on_basic_attack_hit(self, target):
        super().on_basic_attack_hit(target)
         # 20% chance of basic attacks applying stagger
        if random.random() < 0.2:
            target.apply_effect(Stagger(self.messages))
            self.messages.append(f"{self.name}({self.level})'s stagger triggered!")

    def use_ability(self, target):
        super().use_ability(target)
        self.deal_damage(target, 66, DamageType.AD)
        target.apply_effect(Stagger(self.messages))
        self.messages.append(f"{self.name} used its ability on {target.name} and staggering the target!")

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
        for enemy_venari in enemy_team:
            enemy_venari.apply_effect(DefenceDebuff(self.messages, 10, 4))
            enemy_venari.apply_effect(MagicResistDebuff(self.messages, 10, 4))

        self.messages.append(f"{self.name}({self.level}) applied Defence and Magic Resist debuffs to the entire enemy team!")
