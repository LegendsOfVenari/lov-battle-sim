from .aura import Aura
from effect import GracefulEmbraceEffect


class GracefulEmbraceAura(Aura):
    def __init__(self, messages, duration=6, expired=False):
        super().__init__(messages, duration)
        self.arena_effect_id = "graceful_embrace_aura"

    def on_tick(self, venari):
        super().on_tick(venari)
        # Apply Graceful Embrace Aura
        venari.apply_effect(GracefulEmbraceEffect(self.messages))

    def description(self):
        return f"Graceful Embrace: +10 MR, +15 AP, {self.duration} remaining"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return GracefulEmbraceAura(messages,
                                   data["duration"],
                                   data["expired"])
