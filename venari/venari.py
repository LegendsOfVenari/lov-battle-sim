import random
import importlib
from config import venari_base_stats_map
from .battle_handler import BattleHandler
from .battle_stats import BattleStats

class Venari:
    def __init__(self, name, base_stats, level, messages, battle_handler=None, battle_stats=None):
        # Static Values
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.messages = messages

        self.battle_stats = battle_stats or BattleStats(base_stats, level)
        self.battle_handler = battle_handler or BattleHandler(messages)

    def ready_to_attack(self):
        return self.battle_handler.ready_to_attack(self.base_stats["Basic Attack Frequency"])        

    def basic_attack(self, target, auto_attack_buff=0):
        self.battle_handler.attack_tick_counter = 0  # Reset the attack tick counter
        for effect in list(self.battle_handler.active_effects.values()):
            should_proceed = effect.modify_basic_attack(self, target)
            if not should_proceed:
                return  # Stop the basic attack if any effect says to halt

        hit_chance = random.randint(0, 100)
        if hit_chance <= self.battle_stats.accuracy - self.battle_stats.dodge_chance:
            self.deal_auto_attack_damage(target, auto_attack_buff)
            self.on_basic_attack_hit(target)
            # Energy gain from basic attack
            self.battle_handler.gain_energy(self.base_stats["Basic Attack Energy Gain"])
            return True
        else:
            self.on_target_miss(target)
            self.messages.append(f"{self.name}({self.level})'s attack missed {target.name}({target.level})!")
            return False

    def use_ability(self, target):
        self.battle_handler.energy = 0

    def on_swap_in(self, enemy_team=None):
        self.battle_handler.attack_tick_counter = 0
        self.battle_handler.swap_cooldown = 6

    def tick_effects(self):
        """Process all active effects for the Venari."""
        for effect in list(self.battle_handler.active_effects.values()):
            effect.on_tick(self)

    def tick(self, is_point=True):
        """What the Venari does every tick."""

        self.battle_handler.gain_energy(self.base_stats["Energy Gain Passively"])

        self.tick_effects()

        self.battle_handler.tick(is_point, self)

    def apply_effect(self, effect):
        self.battle_handler.apply_effect(effect, self)

    def basic_attack_damage(self):
        return ((((2 * self.level) / 5) *
                 self.base_stats["Basic Attack Movestat"]) / 50) + self.battle_stats.attack_damage + (self.base_stats["Basic Attack Movestat"] / 10)

    def deal_damage(self, target, base_damage, damage_type):
        damage = BattleHandler.calculate_damage(damage_type, self, target, base_damage)
        self.messages.append(f"Dealt {damage}!")
        target.receive_damage(damage)

    def deal_auto_attack_damage(self, target, auto_attack_buff):
        damage = BattleHandler.calculate_basic_attack_damage(self, target, self.base_stats["Basic Attack Damage"] + auto_attack_buff)
        self.messages.append(f"{self.name}({self.level}) attacked {target.name}({target.level}) for {damage:.2f} damage!")
        target.receive_damage(damage)

    def receive_damage(self, damage):
        # Reduce HP
        self.battle_handler.receive_damage(self, damage)

    def on_basic_attack_hit(self, target):
        print("BASIC ATTACK HIT")
        pass

    def on_target_miss(self, target):
        pass

    def serialize_venari(venari):
        """Convert a Venari object into a serializable dictionary."""
        return {
            'name': venari.name,
            'base_stats': venari.base_stats,
            'level': venari.level,
            'battle_handler': venari.battle_handler.serialize(),
            'battle_stats': venari.battle_stats.serialize(),
        }

    @classmethod
    def deserialize_venari(cls, data, messages):
        """Convert a serialized dictionary into a Venari object."""
        name = data['name']
        level = data['level']

        module = importlib.import_module("venari")
        venari_class = getattr(module, name)
        base_stats = venari_base_stats_map.get(name)

        serialized_battle_handler = data.get('battle_handler')
        if serialized_battle_handler:
            battle_handler = BattleHandler.deserialize(serialized_battle_handler, messages)
        else:
            battle_handler = BattleHandler(messages)

        serialized_battle_stats = data.get('battle_stats')
        if serialized_battle_stats:
            battle_stats = BattleStats.deserialize(serialized_battle_stats)
        else:
            battle_stats = BattleStats(base_stats, level)

        venari = venari_class(name, base_stats, level, messages, battle_handler, battle_stats)

        return venari
