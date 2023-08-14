import random
from effect import Stagger
from .battle_utils import calculate_basic_attack_damage, calculate_ability_damage, DamageType

class Venari:
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)

    def __init__(self, name, base_stats, level):
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.level_up()
        self.energy = 0
        self.accuracy = 100  # Start with 100% accuracy
        self.attack_tick_counter = 0
        self.active_effects = []  # List to hold active effects
        self.action_performed = False  # New attribute
        self.ready_to_attack = False  # New attribute to track if Venari is ready to attack
        self.swap_cooldown = 0  # Initially, no cooldown

    def level_up(self):
        """Calculates stats based on level and base stats."""
        self.constitution = ((2 * self.base_stats["Constitution"] * (self.level + 4)) / 100)
        self.attack_damage = ((2 * self.base_stats["Attack Damage"] * (self.level + 4)) / 100)
        self.ability_power = ((2 * self.base_stats["Ability Power"] * (self.level + 4)) / 100)
        self.defense = ((2 * self.base_stats["Defence"] * (self.level + 4)) / 100)
        self.magic_resist = ((2 * self.base_stats["Magic Resist"] * (self.level + 4)) / 100)
        self.hp = 10 * self.level + self.constitution * 15 + 100

    def apply_effect(self, effect):
        # Ensure the effect is not already applied if it's not stackable
        existing_effect = next((e for e in self.active_effects if isinstance(e, effect.__class__)), None)
        if existing_effect and existing_effect.stackable:
            existing_effect.stack()
        else:
            self.active_effects.append(effect)
            effect.on_apply(self)

    def tick_effects(self):
        """Process all active effects for the Venari."""
        for effect in self.active_effects:
            effect.on_tick(self)
            effect.tick()

        # Remove expired effects
        self.active_effects = [effect for effect in self.active_effects if not effect.expired]

    def basic_attack_damage(self):
        return ((((2 * self.level) / 5) * self.base_stats["Basic Attack Movestat"]) / 50) + self.attack_damage + (self.base_stats["Basic Attack Movestat"] / 10)

    def basic_attack(self, target):
        self.action_performed = True
        self.ready_to_attack = False  # Reset the readiness flag after performing the attack
        self.attack_tick_counter = 0  # Reset the attack tick counter

        hit_chance = random.randint(0, 100)
        if hit_chance <= self.accuracy:
            damage = calculate_basic_attack_damage(self, target, self.base_stats["Basic Attack Damage"])
            target.receive_damage(damage)

            # Energy gain from basic attack
            self.energy += self.base_stats["Basic Attack Energy Gain"]
            self.energy = min(self.energy, 100)

            print(f"{self.name}({self.level}) attacked {target.name}({target.level}) for {damage:.2f} damage!")
        else:
            print(f"{self.name}({self.level})'s attack missed {target.name}({target.level})!")

    def use_ability(self, target):
        self.action_performed = True
        self.energy = 0

    def receive_damage(self, damage):
        """Handle receiving damage and interacting with active effects."""
        # Reduce HP
        self.hp -= damage

        # Notify all active effects that damage was received
        for effect in self.active_effects:
            effect.on_damage_received(self, damage)

    def on_swap_in(self, enemy_team=None):
        self.action_performed = True
        self.attack_tick_counter = 0
        self.swap_cooldown = 6

    def tick(self, is_point=True):
        """What the Venari does every tick."""
        self.reset_action()
        self.energy += self.base_stats["Energy Gain Passively"]
        self.energy = min(self.energy, 100)
        self.tick_effects()

        if is_point:
            # Update attack readiness only for the point Venari
            self.attack_tick_counter += 1
            if self.attack_tick_counter >= self.base_stats["Basic Attack Frequency"]:
                self.ready_to_attack = True
                print(f"{self.name}({self.level}) will attack on the next tick!")
        else:
            if self.swap_cooldown > 0:
                self.swap_cooldown -= 1

    def reset_action(self):
        self.action_performed = False

    def can_attack(self):
        disruption_effects = [Stagger]  # Add other disruption effects like Stun here
        for disrupt_effect in disruption_effects:
            if any(isinstance(effect, disrupt_effect) for effect in self.active_effects):
                return (False, disrupt_effect.__name__)

        return (True, None)
