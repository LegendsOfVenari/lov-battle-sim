from effect import Effect, StackableEffect
from config import DamageType
import random

class BattleHandler:
    """
    Handles the battle mechanics, including attacks, effects, and energy management.
    """

    def __init__(self, messages):
        self.energy = 0
        self.attack_tick_counter = 0
        self.active_effects = {}
        self.swap_cooldown = 0
        self.messages = messages

    # ---------------------- ATTACK METHODS ---------------------- #

    def basic_attack(self, attacker, target, auto_attack_buff=0):
        """Performs a basic attack from the attacker to the target."""
        self.attack_tick_counter = 0

        for effect in list(attacker.battle_handler.active_effects.values()):
            should_proceed = effect.modify_basic_attack(attacker, target)
            if not should_proceed:
                return False

        hit_chance = random.randint(0, 100)
        if hit_chance <= attacker.battle_stats.accuracy - attacker.battle_stats.dodge_chance:
            self._deal_auto_attack_damage(attacker, target, auto_attack_buff)
            # Call Back
            attacker.on_basic_attack_hit(target)
            # Basic Attack Energy Gain
            self.gain_energy(attacker.base_stats.basic_attack_energy_gain)
            return True
        else:
            attacker.on_target_miss(target)
            self.messages.append(f"{attacker.name}({attacker.level})'s attack missed {target.name}({target.level})!")
            return False

    def deal_damage(self, attacker, target, base_damage, damage_type, accuracy):
        """Calculates and deals damage from the attacker to the target."""
        hit_chance = random.randint(0, 100)
        if hit_chance <= accuracy - attacker.battle_stats.dodge_chance:
            damage = self._calculate_damage(damage_type, attacker, target, base_damage)
            self.messages.append(f"Dealt {damage} Damage!")
            target.receive_damage(damage)
        else:
            attacker.on_target_miss(target)
            self.messages.append(f"{attacker.name}({attacker.level})'s ability missed {target.name}({target.level})!")

    def receive_damage(self, venari, damage):
        # Notify all active effects that damage was received
        venari.battle_stats.hp = max(0, venari.battle_stats.hp - damage)
        for effect in list(self.active_effects.values()):
            effect.on_damage_received(venari, damage)

    def _deal_auto_attack_damage(self, attacker, target, auto_attack_buff):
        damage = self._calculate_basic_attack_damage(attacker, target, attacker.base_stats.basic_attack_damage + auto_attack_buff)
        self.messages.append(f"{attacker.name}({attacker.level}) attacked {target.name}({target.level}) for {damage:.2f} damage!")
        target.receive_damage(damage)

    def _calculate_basic_attack_damage(self, attacker, target, base_damage):
        attacker_attack_damage = ((2 * attacker.base_stats.attack_damage) * (attacker.level + 4)) / 100
        target_defense = ((2 * target.base_stats.defence) * (target.level + 4)) / 100

        ad_reduction = target_defense / (target_defense + 300)

        ad_multiplier = (((2 * attacker.level) / 5) * base_damage) / 50
        damage = ad_multiplier + attacker_attack_damage + base_damage/10
        return damage * (1 - ad_reduction)

    def _calculate_damage(self, damage_type, attacker, target, base_damage):
        # Calculate reductions
        ap_reduction = target.battle_stats.magic_resist / (target.battle_stats.magic_resist + 300)
        ad_reduction = target.battle_stats.defense / (target.battle_stats.defense + 300)

        # Calculate damage
        if damage_type == DamageType.AD:
            ad_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
            damage = ad_multiplier + attacker.battle_stats.attack_damage + base_damage
            return damage * (1 - ad_reduction)

        elif damage_type == DamageType.AP:
            damage = BattleHandler.calculateAbilityPower(attacker, base_damage)
            return damage * (1 - ap_reduction)

        elif damage_type == DamageType.TRUE_DAMAGE:
            return base_damage
        else:
            raise ValueError("Invalid damage type provided.")

    @classmethod
    def calculateAbilityPower(cls, attacker, base_damage):
        ap_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
        return ap_multiplier + attacker.battle_stats.ability_power + base_damage

    # ---------------------- UTILITY METHODS ---------------------- #

    def ready_to_attack(self, basic_attack_frequency):
        return self.attack_tick_counter >= basic_attack_frequency

    def tick(self, is_point):
        if is_point:
            self.attack_tick_counter += 1
        else:
            if self.swap_cooldown > 0:
                self.swap_cooldown -= 1

    def gain_energy(self, amount):
        self.energy += amount
        self.energy = min(self.energy, 100)

    # ---------------------- EFFECT METHODS ---------------------- #

    def apply_effect(self, effect, venari):
        effect_id = effect.effect_id
        if effect_id in self.active_effects:
            existing_effect = self.active_effects[effect_id]
            existing_effect.on_apply(venari)
        else:
            self.active_effects[effect_id] = effect
            effect.on_apply(venari)

    def remove_stack(self, effect, venari):
        effect_id = effect.effect_id
        if effect in self.active_effects:
            self.active_effects[effect_id].remove_stack(venari)

    def remove_effect(self, effect):
        effect_id = effect.effect_id
        if effect_id in self.active_effects:
            effect = self.active_effects[effect_id]
            effect.remove()

    def has_effect(self, effect):
        effect_id = effect.effect_id
        return effect_id in self.active_effects

    def count_stacks(self, effect_id):
        if effect_id in self.active_effects:
            return self.active_effects[effect_id].count
        else:
            return 0

    def is_effect_stackable(self, effect):
        return isinstance(effect, StackableEffect)

    # ---------------------- UTILITY METHODS ---------------------- #

    def heal(self, venari, amount):
        venari.battle_stats.hp = min(venari.battle_stats.hp + amount, venari.battle_stats.initial_hp)
        self.messages.append(f"Healed {amount} HP!")

    def find_effect_instance(self, effect):
        return next((e for e in self.active_effects if isinstance(e, effect.__class__)), None)

    # ---------------------- SERIALIZATION METHODS ---------------------- #

    def serialize(self):
        return {
            'energy': self.energy,
            'attack_tick_counter': self.attack_tick_counter,
            'active_effects': {key: effect.serialize() for key, effect in self.active_effects.items()},
            'swap_cooldown': self.swap_cooldown
        }

    @classmethod
    def deserialize(cls, data, messages):
        battleHandler = BattleHandler(messages)
        battleHandler.energy = data['energy']
        battleHandler.attack_tick_counter = data['attack_tick_counter']
        battleHandler.active_effects = {key: Effect.deserialize(effect_data, messages) for key, effect_data in data['active_effects'].items()}
        battleHandler.swap_cooldown = data['swap_cooldown']
        return battleHandler
