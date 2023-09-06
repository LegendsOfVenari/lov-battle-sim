from .effect import Effect

class PheremoneTailwindEffect(Effect):
    def __init__(self, messages, duration=1, expired=False, is_permanent=False):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "pheremone_tailwind_effect"

    def description(self):
        return f"Pheremone Tailwind Effect: +1 Attack Speed, +15 AD, {self.duration} seconds remaining"

    def on_apply(self, venari):
        super().on_apply(venari)
        self.duration = 1
        venari.increase_attack_speed(1)
        venari.increase_attack_damage(15)

    def on_remove(self, venari):
        venari.decrease_attack_speed(1)
        venari.decrease_attack_damage(15)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'is_permanent': self.is_permanent
        }

    @classmethod
    def deserialize(cls, data, messages):
        return PheremoneTailwindEffect(messages,
                                       data["duration"],
                                       data["expired"],
                                       data["is_permanent"])
