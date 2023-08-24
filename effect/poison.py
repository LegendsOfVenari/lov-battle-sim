from .stackable_effect import StackableEffect
from config import DamageType


class Poison(StackableEffect):

    def __init__(self,
                 messages,
                 initial_duration=8,
                 duration=8,
                 count=0,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, initial_duration, duration, count, expired)
        self.effect_id = "poison"

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        damage = 0.02 * venari.battle_stats.initial_hp  # 10% of current HP in true damage
        venari.deal_damage(venari, damage, DamageType.TRUE_DAMAGE, 100)
        self.messages.append(f"{venari.name} took {damage:.2f} poison damage!")

    def stack(self):
        super().stack()

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count,
            'expired': self.expired,
            'is_permanent': self.is_permanent
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Poison(messages,
                      data["initial_duration"],
                      data["duration"],
                      data["count"],
                      data["expired"],
                      data["is_permanent"])

