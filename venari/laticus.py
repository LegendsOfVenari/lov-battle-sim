from .venari import Venari
from effect import ArmyOfOne
from config import DamageType


class Laticus(Venari):
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
        if 'army_of_one' not in self.battle_handler.active_effects:
            self.apply_effect(ArmyOfOne(self.messages))

    def use_ability(self, target):
        super().use_ability(target)

        army_of_one = self.get_effect("army_of_one")
        army_of_one.buffed_barrage(self)

        self.messages.append(f"{self.name} used its ability and doubled its stacks.")

        enemy_team = self.battle.get_enemy_team(self)
        for _ in range(5):
            self.deal_damage(enemy_team[0], 5, DamageType.AP, 100)

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()

    def on_ally_ability(self, ally):
        super().on_ally_ability(ally)
        army_of_one = self.get_effect("army_of_one")
        army_of_one.working_colony(self)
