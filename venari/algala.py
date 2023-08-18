from .venari import Venari
from effect import Armor, AttackDamageBuff
from config import DamageType


class Algala(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)

    def on_basic_attack_hit(self, target):
        super().on_basic_attack_hit(target)
        # 20% chance of basic attacks applying stagger
        self.apply_effect(Armor(self.messages))
        self.messages.append(f"{self.name}({self.level})'s gained an armor stack!")

    def use_ability(self, target):
        super().use_ability(target)

        # Calculate the damage based on Algala's Attack Damage (AD)
        self.deal_damage(target, 75, DamageType.AD)
        self.messages.append(f"{self.name} charged recklessly at {target.name}!")

        # Check if Algala has an Armor stack to decide if self-damage is applied
        has_armor = any(isinstance(effect, Armor) for effect in self.battle_handler.active_effects)
        if not has_armor:
            self.deal_damage(self, 75, DamageType.AD)  # Algala takes the same amount of damage
            self.messages.append(f"{self.name} took damage from its own charge!")
        else:
            # Remove one Armor stack from Algala
            for effect in self.battle_handler.active_effects:
                if isinstance(effect, Armor):
                    self.deal_damage(self, 0, DamageType.AD)
                    self.messages.append(f"{self.name}'s Armor stack protected it from self-inflicted damage!")
                    break

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()

        # Calculate the missing health percentage
        max_hp = 10 * self.level + self.battle_stats.constitution * 15 + 100
        missing_hp_percentage = (max_hp - self.battle_stats.hp) / max_hp

        # Calculate the attack damage boost based on the missing health
        boost_amount = (missing_hp_percentage // 0.1) * 10

        if boost_amount > 0:
            self.apply_effect(AttackDamageBuff(boost_amount, self.messages))
            self.messages.append(f"{self.name} gains {boost_amount} AD due to its missing health!")

    def on_swap_out(self):
        for effect in self.active_effects:
            if isinstance(effect, AttackDamageBuff):
                effect.expired = True
                break
