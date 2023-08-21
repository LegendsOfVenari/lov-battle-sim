from effect import Effect, Stagger, StackableEffect
from config import DamageType

class BattleHandler:
    def __init__(self, messages):
        self.energy = 0
        self.attack_tick_counter = 0
        self.active_effects = {}
        self.swap_cooldown = 0
        self.messages = messages

    def receive_damage(self, venari, damage):
        # Notify all active effects that damage was received
        venari.battle_stats.hp = max(0, venari.battle_stats.hp - damage)
        for effect in list(self.active_effects.values()):
            effect.on_damage_received(venari, damage)

    def ready_to_attack(self, basic_attack_frequency):
        return self.attack_tick_counter >= basic_attack_frequency

    def tick(self, is_point, venari):
        if is_point:
            self.attack_tick_counter += 1
            if self.attack_tick_counter >= venari.base_stats["Basic Attack Frequency"]:
                self.messages.append(f"Will attack on the next tick!")
        else:
            if self.swap_cooldown > 0:
                self.swap_cooldown -= 1

    def gain_energy(self, amount):
        self.energy += amount
        self.energy = min(self.energy, 100)
        self.messages.append(f"Gained {amount} Energy passively")

    def remove_stack(self, effect, venari):
        effect_id = effect.EFFECT_ID
        if effect_id in self.active_effects:
            self.active_effects[effect_id].remove_stack(venari)

    def remove_effect(self, effect):
        effect_id = effect.EFFECT_ID
        if effect_id in self.active_effects:
            self.active_effects.pop(effect_id)

    def has_effect(self, effect):
        effect_id = effect.EFFECT_ID
        return effect_id in self.active_effects

    def count_stacks(self, effect):
        effect_id = effect.EFFECT_ID
        if effect_id in self.active_effects:
            return self.active_effects[effect_id].count
        else:
            return 0

    def is_effect_stackable(self, effect):
        return isinstance(effect, StackableEffect)

    def apply_effect(self, effect, venari):
        effect_id = effect.EFFECT_ID
        if effect_id in self.active_effects:
            existing_effect = self.active_effects[effect_id]
            existing_effect.on_apply(venari)
        else:
            self.active_effects[effect_id] = effect
            effect.on_apply(venari)

    def find_effect_instance(self, effect):
        return next((e for e in self.active_effects if isinstance(e, effect.__class__)), None)

    @classmethod
    def calculate_basic_attack_damage(cls, attacker, target, base_damage):
        attacker_attack_damage = ((2 * attacker.base_stats["Attack Damage"]) * (attacker.level + 4)) / 100
        target_defense = ((2 * target.base_stats["Defence"]) * (target.level + 4)) / 100

        ad_reduction = target_defense / (target_defense + 300)

        ad_multiplier = (((2 * attacker.level) / 5) * base_damage) / 50
        damage = ad_multiplier + attacker_attack_damage + base_damage/10
        return damage * (1 - ad_reduction)

    @classmethod
    def calculate_damage(cls, damage_type, attacker, target, base_damage):
        # Calculate reductions
        ap_reduction = target.battle_stats.magic_resist / (target.battle_stats.magic_resist + 300)
        ad_reduction = target.battle_stats.defense / (target.battle_stats.defense + 300)
        print(damage_type)
        # Calculate damage
        if damage_type == DamageType.AD:
            ad_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
            damage = ad_multiplier + attacker.battle_stats.attack_damage + base_damage
            return damage * (1 - ad_reduction)

        elif damage_type == DamageType.AP:
            ap_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
            damage = ap_multiplier + attacker.battle_stats.ability_power + base_damage
            return damage * (1 - ap_reduction)

        elif damage_type == DamageType.TRUE_DAMAGE:
            return base_damage
        else:
            raise ValueError("Invalid damage type provided.")

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
