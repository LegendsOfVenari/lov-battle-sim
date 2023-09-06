from .venari import Venari
from effect import GatheringDust, AccuracyDebuff
from config import DamageType
from arena_effect import PheremoneTailwindAura


class Vespille(Venari):

    def on_ally_basic_attack(self, attacker):
        self.reduce_swap_cooldown(1)

    def basic_attack(self, target):
        super().basic_attack(target)

    def use_ability(self, target):
        super().use_ability(target)
        self.battle.add_ally_arena_effect(PheremoneTailwindAura(self.messages), self)
        self.messages.append(f"{self.name} used its ability on {target.name}!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.battle.remove_ally_arena_effect("trap", self)
        self.battle.remove_ally_arena_effect("heavy_trap", self)
