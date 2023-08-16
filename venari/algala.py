from .venari import Venari
from effect import Armor, AttackDamageBuff
from .battle_utils import calculate_basic_attack_damage, calculate_ability_damage, DamageType

class Algala(Venari):
    def basic_attack(self, target, messages):
        super().basic_attack(target, messages)

        # 20% chance of basic attacks applying stagger
        self.apply_effect(Armor(), messages)
        messages.append(f"{self.name}({self.level})'s gained an armor stack!")

    def use_ability(self, target, messages):
        super().use_ability(target, messages)

        # Calculate the damage based on Algala's Attack Damage (AD)
        damage = calculate_ability_damage(DamageType.AD, self, target, 75)

        # Apply damage to the target
        target.receive_damage(damage)
        messages.append(f"{self.name} charged recklessly at {target.name}, dealing {damage:.2f} damage!")

        # Check if Algala has an Armor stack to decide if self-damage is applied
        has_armor = any(isinstance(effect, Armor) for effect in self.active_effects)
        if not has_armor:
            self.receive_damage(damage)  # Algala takes the same amount of damage
            messages.append(f"{self.name} took {damage:.2f} damage from its own charge!")
        else:
            # Remove one Armor stack from Algala
            for effect in self.active_effects:
                if isinstance(effect, Armor):
                    effect.on_damage_received(self, damage, messages)
                    messages.append(f"{self.name}'s Armor stack protected it from self-inflicted damage!")
                    break

    def on_swap_in(self, messages, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in(messages)

        # Calculate the missing health percentage
        max_hp = 10 * self.level + self.constitution * 15 + 100
        missing_hp_percentage = (max_hp - self.hp) / max_hp

        # Calculate the attack damage boost based on the missing health
        boost_amount = (missing_hp_percentage // 0.1) * 10

        if boost_amount > 0:
            self.apply_effect(AttackDamageBuff(boost_amount), messages)
            messages.append(f"{self.name} gains {boost_amount} AD due to its missing health!")

    def on_swap_out(self):
        for effect in self.active_effects:
            if isinstance(effect, AttackDamageBuff):
                effect.expired = True
                break
