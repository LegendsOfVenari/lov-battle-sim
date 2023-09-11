from .venari import Venari
from effect import Stagger
from config import DamageType

class Togoe(Venari):
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

    # Implement the passive here
    def apply_effect(self, effect):
        if effect.effect_id == "ability_power_static_buff":
            effect.increase_amount *= 2
        super().apply_effect(effect)

    def use_ability(self, target):
        super().use_ability(target)
        enemy_team = self.battle.get_enemy_team(self)
        for enemy in enemy_team:
            self.deal_damage(enemy, 15, DamageType.AP, 100)
        self.messages.append(f"{self.name} used its ability, dealing 15 AP damage to each enemy Venari!")

    def on_swap_in(self, enemy_team=None):
        super().on_swap_in()
