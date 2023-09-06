from .stackable_effect import StackableEffect
from config import DamageType


class Poison(StackableEffect):

    def __init__(self,
                 messages,
                 level,
                 ability_power,
                 initial_duration=6,
                 duration=6,
                 count=0,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, initial_duration, duration, count, expired)
        self.level = level
        self.ability_power = ability_power
        self.effect_id = "poison"

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        total_damage = venari.battle_handler.calculate_ability_power(self.level, self.ability_power, 10)
        total_damage = total_damage / self.initial_duration
        venari.deal_effect_damage(DamageType.AP, venari, total_damage)
        self.messages.append(f"{venari.name} took {total_damage:.2f} poison damage!")

    def stack(self):
        super().stack()

    def calculate_total_remaining_damage(self, venari):
        total_damage = venari.battle_handler.calculate_ability_power(self.level, self.ability_power, 10)
        total_damage = total_damage / self.initial_duration
        total_damage *= self.duration
        if self.count > 1:
            total_damage += venari.battle_handler.calculate_ability_power(self.level, self.ability_power, 10) * self.count - 1
        return total_damage

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'level': self.level,
            'ability_power': self.ability_power,
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count,
            'expired': self.expired,
            'is_permanent': self.is_permanent
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Poison(messages,
                      data["level"],
                      data["ability_power"],
                      data["initial_duration"],
                      data["duration"],
                      data["count"],
                      data["expired"],
                      data["is_permanent"])
