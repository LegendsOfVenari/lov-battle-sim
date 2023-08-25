from .effect import Effect

class DustCloudEffect(Effect):
    def __init__(self, messages, dodge_chance, duration=1, expired=False, is_permanent=False):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "dust_cloud_effect"
        self.dodge_chance = dodge_chance

    def description(self):
        return f"Dust Cloud: Grants {self.dodge_chance}% dodge chance, {self.duration} seconds remaining"

    def on_apply(self, venari):
        super().on_apply(venari)
        venari.increase_dodge_chance(self.dodge_chance)

    def on_remove(self, venari):
        venari.decrease_dodge_chance(self.dodge_chance)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'dodge_chance': self.dodge_chance
        }

    @classmethod
    def deserialize(cls, data, messages):
        return DustCloudEffect(messages,
                               data["dodge_chance"],
                               data["duration"],
                               data["expired"],
                               data["is_permanent"])