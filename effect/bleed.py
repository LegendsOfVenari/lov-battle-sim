from .stackable_effect import StackableEffect
from config import DamageType


class Bleed(StackableEffect):

    def __init__(self,
                 messages,
                 damage,
                 initial_duration=3,
                 duration=3,
                 count=0,
                 expired=False):
        super().__init__(messages, initial_duration, duration, count, expired)
        self.damage = damage
        self.effect_id = "bleed"

    def description(self):
        return f"Bleed ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        damage = self.damage / 3
        venari.deal_damage(venari, damage, DamageType.AD, 100)
        self.messages.append(f"{venari.name} took bleed damage!")

    def stack(self):
        super().stack()

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'damage': self.damage,
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Bleed(messages,
                      data["initial_duration"],
                      data["duration"],
                      data["count"],
                      data["expired"])

