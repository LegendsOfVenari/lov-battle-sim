from .aura import Aura
from effect import GracefulEmbraceEffect


class GracefulEmbraceAura(Aura):
    def __init__(self, messages, duration=6, expired=False, heal_tick=0):
        super().__init__(messages, duration)
        self.heal_amount = heal_tick
        self.arena_effect_id = "graceful_embrace_aura"

    def on_tick(self, venari):
        super().on_tick(venari)
        # Apply Graceful Embrace Aura
        venari.apply_effect(GracefulEmbraceEffect(self.messages,
                                                  heal_amount=self.heal_amount))

    def description(self):
        return f"Graceful Embrace: {round(self.heal_amount, 2)} HP, {self.duration} remaining"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'heal_amount': self.heal_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return GracefulEmbraceAura(messages,
                                   data["duration"],
                                   data["expired"],
                                   data["heal_amount"])
