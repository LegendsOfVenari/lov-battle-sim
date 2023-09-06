from .aura import Aura
from effect import PheremoneTailwindEffect

class PheremoneTailwindAura(Aura):
    def __init__(self, messages, duration=6, expired=False):
        super().__init__(messages, duration, expired)
        self.arena_effect_id = "pheremone_tailwind_aura"

    def on_tick(self, venari):
        super().on_tick(venari)
        venari.apply_effect(PheremoneTailwindEffect(self.messages))

    def description(self):
        return f"Pheremone Tailwind Aura: +1 Attack Speed, 15 AD, {self.duration} ticks remaining"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return PheremoneTailwindAura(messages, data["duration"], data["expired"])
