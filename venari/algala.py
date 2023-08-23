from .venari import Venari
from effect import Armor, AttackDamageBuff
from config import DamageType


class Algala(Venari):
    def basic_attack(self, target):
        super().basic_attack(target)

    def armor(self):
        return Armor(self.messages)

    def attack_damage_buff(self):
        return AttackDamageBuff(10, self.messages)

    def on_basic_attack_hit(self, target):
        super().on_basic_attack_hit(target)
        self.apply_effect(Armor(self.messages))
        self.messages.append(f"{self.name}({self.level})'s gained an armor stack!")

    def use_ability(self, target):
        super().use_ability(target)

        # Calculate the damage based on Algala's Attack Damage (AD)
        self.deal_damage(target, 75, DamageType.AD, 100)
        self.messages.append(f"{self.name} charged recklessly at {target.name}!")

        # Check if Algala has an Armor stack to decide if self-damage is applied
        if not self.battle_handler.has_effect(self.armor()):
            self.deal_damage(self, 75, DamageType.AD, 100)  # Algala takes the same amount of damage
            self.messages.append(f"{self.name} took damage from its own charge!")
        else:
            # Remove one Armor stack from Algala
            self.battle_handler.remove_stack(self.armor(), self)
            self.messages.append(f"{self.name}'s Armor stack protected it from self-inflicted damage!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()

        missing_hp_percentage = (self.battle_stats.initial_hp - self.battle_stats.hp) / self.battle_stats.initial_hp

        # Calculate the boosts based on every 15% missing hp
        bonus_factor = missing_hp_percentage // 0.15

        if bonus_factor > 0:
            self.apply_effect(AttackDamageBuff(10 * bonus_factor, self.messages))
            for _ in range(int(bonus_factor)):
                self.apply_effect(self.armor())
            self.messages.append(f"{self.name} gains {bonus_factor} Armor due to its missing health!")

    def on_swap_out(self):
        self.battle_handler.remove_effect(self.attack_damage_buff())
