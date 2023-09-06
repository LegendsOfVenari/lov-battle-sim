from .venari import Venari
from effect import Unique
from config import DamageType
from arena_effect import Trap, HeavyTrap

class Folicri(Venari):

    def on_enemy_ability(self, enemy):
        if self.battle.has_arena_effect("trap", self):
            self._add_stockpile()
        else:
            self.battle.add_enemy_arena_effect(Trap(self.messages), self)


    def use_ability(self, target):
        super().use_ability(target)
        self.messages.append(f"{self.name} used its ability on {target.name}!")

        if self.battle.has_arena_effect("trap", self):
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
        self._add_stockpile()
        self.deal_damage(enemy_team[0], 10, DamageType.AP, 100)

    def _add_stockpile(self):
        self.apply_effect(Unique(self.messages, "stockpile", None, None, 0, False, False, 5))
