from .effect import Effect
from config import DamageType


class Web(Effect):

    def __init__(self,
                 messages,
                 duration,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, duration, expired, is_permanent)
        self.effect_id = "web"

    def description(self):
        return f"Webbed ({self.duration} ticks)"

    def modify_swap(self):
        """Returns a boolean indicating if the swap should proceed."""
        return True

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

        return Web(messages,
                   data["duration"],
                   data["expired"],
                   data["is_permanent"])
