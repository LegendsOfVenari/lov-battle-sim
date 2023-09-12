from .stackable_effect import StackableEffect
from config import DamageType


class Bleed(StackableEffect):

    def __init__(self,
                 messages,
                 level,
                 attack_damage,
                 initial_duration=3,
                 duration=3,
                 count=0,
                 expired=False):
        super().__init__(messages, initial_duration, duration, count, expired)
        self.level = level
        self.attack_damage = attack_damage
        self.effect_id = "bleed"

    def description(self):
        return f"Bleed ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        total_damage = venari.battle_handler.calculate_attack_damage(self.level, self.attack_damage, 10)
        total_damage = total_damage / self.initial_duration
        venari.deal_effect_damage(DamageType.AD, venari, total_damage)
        self.messages.append(f"{venari.name} took bleed damage!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count,
            'expired': self.expired,
            'level': self.level,
            'attack_damage': self.attack_damage
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Bleed(messages,
                     data["level"],
                     data["attack_damage"],
                     data["initial_duration"],
                     data["duration"],
                     data["count"],
                     data["expired"])
