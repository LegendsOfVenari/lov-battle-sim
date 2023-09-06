from .effect import Effect

class Silence(Effect):

    def __init__(self,
                 messages,
                 duration=3,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "silence"

    def description(self):
        return f"Silence, ({self.duration}) ticks"

    def on_apply(self, venari):
        super().on_apply(venari)

    def modify_ability(self, venari):
        self.messages.append(f"{venari.name}({venari.level}) has been silenced")
        return True  # Abilities do not proceed

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
        return Silence(messages,
                       data["duration"],
                       data["expired"],
                       data["is_permanent"])
