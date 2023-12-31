from .effect import Effect

class Stagger(Effect):

    def __init__(self,
                 messages,
                 duration=3,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, duration, expired)
        self.effect_id = "stagger"

    def description(self):
        return f"Stagger, {self.duration} ticks)"

    def on_apply(self, venari):
        super().on_apply(venari)

    def modify_auto_attack(self, venari):
        self.messages.append(f"{venari.name}({venari.level}) has been staggered")
        # remove the effect after it's triggered
        self.remove()
        return True  # Basic attack does not proceed

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
        return Stagger(messages,
                       data["duration"],
                       data["expired"],
                       data["is_permanent"])

