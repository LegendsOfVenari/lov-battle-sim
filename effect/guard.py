from .effect import Effect


class Guard(Effect):

    def __init__(self,
                 messages,
                 duration,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "guard"

    def description(self):
        return f"Guard ({self.duration} ticks)"

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

        return Guard(messages,
                     data["duration"],
                     data["expired"],
                     data["is_permanent"])
