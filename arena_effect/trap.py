from .arena_effect import ArenaEffect
from effect import TrapEffect
from config import DamageType


class Trap(ArenaEffect):
    def __init__(self, messages, duration=6, expired=False):
        super().__init__(messages, duration, expired)
        self.arena_effect_id = "trap"

    def on_swap_in(self, venari):
        self.messages.append(f"{venari.name} stepped on a Trap!")
        venari.apply_effect(TrapEffect(self.messages))
        venari.deal_damage(venari, 10, DamageType.AD, 100)
        self.remove()

    def description(self):
        return "Trap: {self.duration} Duration"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Trap(messages,
                    data["duration"],
                    data["expired"])
