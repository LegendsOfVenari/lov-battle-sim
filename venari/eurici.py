from .venari import Venari
from effect import Web, Armor, Silence
from config import (
    DamageType,
    enveloping_cocoon_base_damage,
    enveloping_cocoon_damage_type,
    enveloping_cocoon_accuracy,
    enveloping_cocoon_duration,
    whispered_hush_duration
)


class Eurici(Venari):

    def use_ability(self, target):
        super().use_ability(target)
        self.deal_damage(
            target,
            enveloping_cocoon_base_damage,
            enveloping_cocoon_damage_type,
            enveloping_cocoon_accuracy
        )
        # web all enemies
        for enemy in self.battle.get_enemy_team(self):
            enemy.apply_effect(Web(self.messages, enveloping_cocoon_duration))

        self.apply_effect(Armor(self.messages))

        self.messages.append(f"{self.name} used its ability!")

    def on_swap_in(self, enemy_team=None):
        # Call the base class's method to reset the attack tick counter
        super().on_swap_in()
        enemy_venari = self.get_enemy_point_venari()
        enemy_venari.apply_effect(Web(self.messages, whispered_hush_duration))
        self.apply_effect(Armor(self.messages))
