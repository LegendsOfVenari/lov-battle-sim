from .stackable_effect import StackableEffect
from config import DamageType, poison_duration, poison_ability_damage


class Poison(StackableEffect):

    def __init__(self,
                 messages,
                 level,
                 ability_power,
                 initial_duration=poison_duration,
                 duration=poison_duration,
                 count=0,
                 expired=False):
        super().__init__(messages, initial_duration, duration, count, expired)
        self.level = level
        self.ability_power = ability_power
        self.effect_id = "poison"

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        total_damage = venari.battle_handler.calculate_ability_power(
            self.level, self.ability_power, 10
        )
        total_damage = total_damage / self.initial_duration
        venari.deal_effect_damage(DamageType.AP, venari, total_damage)
        self.messages.append(f"{venari.name} took {total_damage:.2f} poison damage!")

    def reset_duration(self):
        self.duration = poison_duration

    def stack(self):
        super().stack()

    def calculate_total_remaining_damage(self, venari):
        total_damage = venari.battle_handler.calculate_ability_power(
            self.level, self.ability_power, poison_ability_damage
        )
        total_damage = total_damage / self.initial_duration
        total_damage *= self.duration
        if self.count > 1:
            additional_damage = venari.battle_handler.calculate_ability_power(
                self.level, self.ability_power, poison_ability_damage
            )
            total_damage += additional_damage * self.count - 1
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
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Poison(messages,
                      data["level"],
                      data["ability_power"],
                      data["initial_duration"],
                      data["duration"],
                      data["count"],
                      data["expired"])
