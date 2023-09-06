from .venari import Venari
from effect import GatheringDust, AccuracyDebuff
from config import DamageType
from arena_effect import DustCloudAura


class Vespille(Venari):

    def on_ally_basic_attack(self, attacker):
        self.reduce_swap_cooldown(1)

    def basic_attack(self, target):
        super().basic_attack(target)
        self.apply_effect(GatheringDust(self.messages))

    def use_ability(self, target):
        super().use_ability(target)
        target.apply_effect(AccuracyDebuff(self.messages, 6, 50))

        effect = self.get_effect("gathering_dust")
        if effect:
            num_stacks = effect.count
            self.battle.add_ally_arena_effect(DustCloudAura(self.messages, num_stacks * 10), self)
            effect.reset()

        self.messages.append(f"{self.name} used its ability on {target.name}!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        self.deal_damage(enemy_team[0], 20, DamageType.AD, 100)
        enemy_team[0].apply_effect(AccuracyDebuff(self.messages, 3, 20))
