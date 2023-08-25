from .venari import Venari
from effect import GatheringDust, AccuracyDebuff
from config import DamageType
from arena_effect import DustCloudAura


class Vespille(Venari):
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
        if 'gathering_dust' not in self.battle_handler.active_effects:
            self.apply_effect(GatheringDust(self.messages))

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
