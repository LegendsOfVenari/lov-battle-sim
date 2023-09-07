from .venari import Venari
from effect import Armor, Stun, BoarSkin
from config import DamageType


class Algala(Venari):
    def __init__(self,
                 name,
                 base_stats,
                 level,
                 messages,
                 isPlayerVenari,
                 battle=None,
                 battle_handler=None,
                 battle_stats=None):
        super().__init__(name,
                         base_stats,
                         level,
                         messages,
                         isPlayerVenari,
                         battle,
                         battle_handler,
                         battle_stats)
        if 'boar_skin' not in self.battle_handler.active_effects:
            self.apply_effect(BoarSkin(self.messages))

    def basic_attack(self, target):
        super().basic_attack(target)

    def armor(self):
        return Armor(self.messages)

    def on_basic_attack_hit(self, target):
        super().on_basic_attack_hit(target)

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

        enemy_team[0].apply_effect(Stun(self.messages))
        self.deal_damage(self, self.battle_stats.max_health * 0.1, DamageType.AD, 100)
