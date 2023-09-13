from .venari import Venari
from effect import Unique
from config import DamageType
from arena_effect import Trap, HeavyTrap

class Folicri(Venari):

    def on_enemy_ability(self, enemy):
        # Should this only be on point/assist only?
        if enemy.battle.has_arena_effect("trap", enemy):
            self._add_stockpile()
        elif not enemy.battle.has_arena_effect("heavy_trap", enemy) and self.is_ally_point_venari():
            # Can only place a trap down when no other trap is active
            self.battle.add_enemy_arena_effect(Trap(self.messages), self)

    def use_ability(self, target):
        super().use_ability(target)
        self.messages.append(f"{self.name} used its ability on {target.name}!")

        if target.battle.has_arena_effect("trap", target):
            heal_amount = self.battle_handler.calculate_ability_power(self.level, self.battle_stats.ability_power, 15)
            self.heal(heal_amount)
            self.messages.append(f"Healed Folicri for {heal_amount} health!")
            self.battle.remove_arena_effect("trap", self)
            self._add_stockpile()
            stockpile_effect = self.get_effect("stockpile")
            if stockpile_effect is not None:
                stockpile_stacks = stockpile_effect.count
                self.battle.add_enemy_arena_effect(HeavyTrap(self.messages, stockpile_stacks), self)
            else:
                self.battle.add_enemy_arena_effect(HeavyTrap(self.messages, 0), self)
        else:
            stockpile_effect = self.get_effect("stockpile")
            if stockpile_effect is not None:
                stockpile_stacks = stockpile_effect.count
                self.battle.add_enemy_arena_effect(HeavyTrap(self.messages, stockpile_stacks), self)
            else:
                self.battle.add_enemy_arena_effect(HeavyTrap(self.messages, 0), self)
            self.remove_effect_id("stockpile")

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
        self.battle.add_enemy_arena_effect(Trap(self.messages), self)

    def _add_stockpile(self):
        self.apply_effect(Unique(self.messages, "stockpile", None, None, 0, False, False, 5))
