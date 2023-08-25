from .aura import Aura
from effect import ReadyToHelpEffect


class ReadyToHelpAura(Aura):
    def __init__(self, messages, duration=6, expired=False, heal_tick=0):
        super().__init__(messages, duration)
        self.heal_amount = heal_tick
        self.arena_effect_id = "ready_to_help_aura"

    def on_tick(self, venari):
        super().on_tick(venari)
        # Apply Ready To Help Effect
        print("Ready to help on tick")
        venari.apply_effect(ReadyToHelpEffect(self.messages,
                                              heal_amount=self.heal_amount))

    def description(self):
        return f"Ready To Help: {round(self.heal_amount, 2)} HP, +1 Attack Speed, {self.duration} remaining"

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
        return ReadyToHelpAura(messages,
                               data["duration"],
                               data["expired"],
                               data["heal_amount"])
