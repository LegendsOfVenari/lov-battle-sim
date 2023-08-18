from .effect import Effect
from config import DamageType


class Poison(Effect):
    def __init__(self, messages, duration=0, count=0):
        super().__init__(True, messages, duration, count)

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        super().on_tick(venari)
        damage = 0.1 * venari.battle_stats.hp  # 10% of current HP in true damage
        venari.deal_damage(venari, damage, DamageType.TRUE_DAMAGE)
        self.messages.append(f"{venari.name} took {damage:.2f} poison damage!")

    def stack(self):
        super().stack()
        self.duration += 6

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'stackable': self.stackable,
            'duration': self.duration,
            'count': self.count,
            'description': self.description()
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Poison(messages,
                      data["duration"],
                      data["count"])
