from .effect import Effect
from config import moonlight_vigor_duration

class MoonlightVigor(Effect):
    def __init__(self,
                 messages,
                 heal_amount,
                 duration=moonlight_vigor_duration,
                 expired=False):
        super().__init__(messages, duration, expired, False)
        self.effect_id = "moonlight_vigor"
        self.heal_amount = heal_amount

    def description(self):
        return f"Moonlight Vigor: {round(self.heal_amount, 2)} HP, {self.duration} remaining"

    def on_apply(self, venari):
        super().on_apply(venari)

        # Refresh Duration
        self.duration = moonlight_vigor_duration

    def on_tick(self, venari):
        super().on_tick(venari)
        # Heal Venari
        venari.heal(self.heal_amount / moonlight_vigor_duration)

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
        print(data)
        return MoonlightVigor(messages,
                              data["heal_amount"],
                              data["duration"],
                              data["expired"])
