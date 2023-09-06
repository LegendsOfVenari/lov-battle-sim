from .arena_effect import ArenaEffect
from effect import TrapEffect
from config import DamageType


class HeavyTrap(ArenaEffect):
    def __init__(self, messages, stockpile_stacks, duration=6, expired=False):
        super().__init__(messages, duration, expired)
        self.stockpile_stacks = stockpile_stacks
        self.arena_effect_id = "heavy_trap"

    def on_swap_in(self, venari):
        self.messages.append(f"{venari.name} stepped on a Heavy Trap!")
        venari.apply_effect(TrapEffect(self.messages))
        venari.deal_damage(venari, 25 + 3 * self.stockpile_stacks, DamageType.AD, 100)
        self.remove()

    def description(self):
        return f"Heavy Trap: {self.stockpile_stacks} Stacks {self.duration} Duration"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'stockpile_stacks': self.stockpile_stacks
        }

    @classmethod
    def deserialize(cls, data, messages):
        return HeavyTrap(messages,
                         data["stockpile_stacks"],
                         data["duration"],
                         data["expired"])
