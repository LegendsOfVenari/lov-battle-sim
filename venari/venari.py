import random
import importlib
from .battle_handler import BattleHandler
from stats import BattleStats, BaseStats

class Venari:
    def __init__(self, name, base_stats, level, messages, isPlayerVenari, battle=None, battle_handler=None, battle_stats=None):
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.messages = messages
        self.isPlayerVenari = isPlayerVenari
        self.battle = battle

        self.battle_stats = battle_stats or BattleStats(base_stats, level)
        self.battle_handler = battle_handler or BattleHandler(messages)

    # Team Methods
    def is_ally_point_venari(self):
        ally_point_venari = self.get_ally_point_venari()
        return ally_point_venari is self

    def get_ally_point_venari(self):
        if self.isPlayerVenari:
            return self.battle.team1[0]
        else:
            return self.battle.team2[0]

    def get_enemy_point_venari(self):
        if self.isPlayerVenari:
            return self.battle.team2[0]
        else:
            return self.battle.team1[0]

    def get_ally_team(self):
        if self.isPlayerVenari:
            return [venari for venari in self.battle.team1 if venari.is_alive()]
        else:
            return [venari for venari in self.battle.team2 if venari.is_alive()]

    def get_enemy_team(self):
        if self.isPlayerVenari:
            return [venari for venari in self.battle.team2 if venari.is_alive()]
        else:
            return [venari for venari in self.battle.team1 if venari.is_alive()]

    def get_ally_bench(self):
        team = self.get_ally_team()
        return team[1:]  # Return all venari except the first one (point venari)

    # Battle Handler methods

    def basic_attack(self, target, auto_attack_buff=0):
        self.battle_handler.basic_attack(self, target, auto_attack_buff)

    def use_ability(self, target):
        self.battle_handler.energy = 0

        # Call back method
        ally_team = self.get_ally_team()
        for venari in ally_team:
            if venari is not self:
                venari.on_ally_ability(self)
        enemy_team = self.get_enemy_team()
        for venari in enemy_team:
            if venari is not self:
                venari.on_enemy_ability(self)

    def apply_effect(self, effect):
        self.battle_handler.apply_effect(effect, self)

    def deal_damage(self, target, base_damage, damage_type, accuracy):
        self.battle_handler.deal_damage(self,
                                        target,
                                        base_damage,
                                        damage_type,
                                        accuracy)

    def deal_effect_damage(self, damage_type, target, total_damage):
        self.battle_handler.deal_effect_damage(damage_type, target, total_damage)

    def ready_to_attack(self):
        return self.battle_handler.ready_to_attack(
            self.battle_stats.attack_speed
        )

    def is_alive(self):
        return self.battle_stats.hp > 0

    def receive_damage(self, damage):
        self.battle_handler.receive_damage(self, damage)

    def heal(self, amount):
        self.battle_handler.heal(self, amount)

    def gain_energy(self, amount):
        self.battle_handler.gain_energy(amount)

    def reduce_swap_cooldown(self, amount):
        self.battle_handler.reduce_swap_cooldown(amount)

    def increase_attack_speed(self, amount):
        self.battle_handler.increase_attack_speed(amount)

    def decrease_attack_speed(self, amount):
        self.battle_handler.decrease_attack_speed(amount)

    # Effect Methods

    def get_effect(self, effect_id):
        return self.battle_handler.get_effect(effect_id)

    def has_effect_id(self, effect_id):
        return self.battle_handler.has_effect_id(effect_id)

    def remove_effect_id(self, effect_id):
        self.battle_handler.remove_effect_id(effect_id)

    # Modifier Methods

    def can_use_ability(self):
        """Determine if a Venari can use its ability based on its effects."""
        for effect in self.battle_handler.active_effects.values():
            if effect.modify_ability(self):
                return False
        return self.battle_handler.energy == 60

    def can_auto_attack(self):
        """Determine if a Venari can auto attack based on its effects."""
        for effect in self.battle_handler.active_effects.values():
            if effect.modify_auto_attack(self):
                return False
        return True

    def can_swap(self):
        """Determine if a Venari can swap based on its effects."""
        if self.is_alive() is False:
            return False
        for effect in self.battle_handler.active_effects.values():
            if effect.modify_swap():
                return False
        if self.battle is not None:
            for venari in self.battle.get_ally_team(self):
                if venari.battle_handler.is_assist:
                    return False
        return self.battle_handler.swap_cooldown == 0

    # Callback methods

    def on_basic_attack_hit(self, target):
        pass

    def on_target_miss(self, target):
        pass

    def on_swap_in(self, enemy_team=None):
        # Do not trigger abilities if venari cannot be swapped in
        if not self.can_swap():
            self.messages.append(f"{self.name}({self.level}) cannot trigger its swap ability!")
            return

    def on_swap_out(self):
        self.battle_handler.swap_cooldown = 12

    def on_ally_basic_attack(self, attacker):
        pass

    def on_enemy_ability(self, enemy):
        pass

    def on_ally_ability(self, ally):
        pass

    def swap_to_point(self):
        self.battle_handler.attack_tick_counter = 100
        self.battle.swap_venari(self)
        self.battle_handler.is_assist = False
        self.battle_handler.assist_cooldown = 6

    # Tick methods

    def tick_effects(self):
        """Process all active effects for the Venari."""
        for effect in list(self.battle_handler.active_effects.values()):
             # Remove any expired effects
            if effect.expired and not effect.is_permanent:
                effect.on_remove(self)
                self.battle_handler.active_effects.pop(effect.effect_id)
            else:
                effect.on_tick(self)
                if effect.expired and not effect.is_permanent:
                    effect.on_remove(self)
                    self.battle_handler.active_effects.pop(effect.effect_id)

    def tick(self, is_point=True):
        """What the Venari does every tick."""
        # Swap point venari with assist venari if need be
        if self.battle_handler.is_assist and self.battle_handler.assist_cooldown == 0:
            self.swap_to_point()

        self.battle_handler.gain_energy(self.base_stats.passive_energy_gain)

        self.tick_effects()

        self.battle_handler.tick(is_point)

    # Serialization

    def serialize_venari(venari):
        """Convert a Venari object into a serializable dictionary."""
        return {
            'name': venari.name,
            'base_stats': venari.base_stats.serialize(),
            'level': venari.level,
            'isPlayerVenari': venari.isPlayerVenari,
            'battle_handler': venari.battle_handler.serialize(),
            'battle_stats': venari.battle_stats.serialize(),
            'can_swap': venari.can_swap(),
            'can_use_ability': venari.can_use_ability()
        }

    @classmethod
    def deserialize_venari(cls, data, messages, battle=None):
        """Convert a serialized dictionary into a Venari object."""
        name = data['name']
        level = data['level']
        isPlayerVenari = data['isPlayerVenari']

        module = importlib.import_module("venari")
        venari_class = getattr(module, name)

        base_stats = BaseStats.deserialize(data['base_stats'])

        serialized_battle_handler = data.get('battle_handler')
        if serialized_battle_handler:
            battle_handler = BattleHandler.deserialize(
                serialized_battle_handler,
                messages
            )
        else:
            battle_handler = BattleHandler(messages)

        serialized_battle_stats = data.get('battle_stats')
        if serialized_battle_stats:
            battle_stats = BattleStats.deserialize(serialized_battle_stats)
        else:
            battle_stats = BattleStats(base_stats, level)

        venari = venari_class(name,
                              base_stats,
                              level,
                              messages,
                              isPlayerVenari,
                              battle,
                              battle_handler,
                              battle_stats)

        return venari
