from .effect import Effect


class GracefulEmbraceEffect(Effect):
    def __init__(self,
                 messages,
                 duration=1,
                 expired=False,
                 heal_amount=0):
        super().__init__(messages, duration, expired, False)
        self.effect_id = "graceful_embrace_effect"
        self.heal_amount = heal_amount

    def description(self):
        return f"Ready To Help: {round(self.heal_amount, 2)} HP, {self.duration} remaining"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Refresh Duration
        self.duration = 1
        venari.increase_magic_resist(10)
        venari.increase_ability_power(15)

    def on_remove(self, venari):
        venari.decrease_magic_resist(10)
        venari.decrease_ability_power(15)

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
        return GracefulEmbraceEffect(messages,
                                    data["duration"],
                                    data["expired"],
                                    data["heal_amount"])
