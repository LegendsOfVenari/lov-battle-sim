from .stackable_effect import StackableEffect
from config import DamageType


class Poison(StackableEffect):
    EFFECT_ID = "poison"

    def __init__(self, messages, initial_duration=8, duration=8, count=0):
        super().__init__(messages, initial_duration, duration, count)

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        damage = 0.1 * venari.battle_stats.hp  # 10% of current HP in true damage
        venari.deal_damage(venari, damage, DamageType.TRUE_DAMAGE)
        self.messages.append(f"{venari.name} took {damage:.2f} poison damage!")

    def stack(self):
        super().stack()

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count
        }

    @classmethod
    def deserialize(cls, data, messages):

        return Poison(messages,
                      data["initial_duration"],
                      data["duration"],
                      data["count"])
