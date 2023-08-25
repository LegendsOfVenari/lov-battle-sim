from .effect import Effect


class ReadyToHelpEffect(Effect):
    def __init__(self,
                 messages,
                 duration=1,
                 expired=False,
                 is_permanent=False,
                 heal_amount=0):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "ready_to_help_effect"
        self.heal_amount = heal_amount

    def description(self):
        return f"Ready To Help: {round(self.heal_amount, 2)} HP, +1 Attack Speed, {self.duration} remaining"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Refresh Duration
        self.duration = 1
        venari.increase_attack_speed(1)

    def on_remove(self, venari):
        venari.decrease_attack_speed(1)

    def on_tick(self, venari):
        super().on_tick(venari)
        # Heal Venari
        venari.heal(self.heal_amount)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'heal_amount': self.heal_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return ReadyToHelpEffect(messages,
                                data["duration"],
                                data["expired"],
                                data["is_permanent"],
                                data["heal_amount"])
