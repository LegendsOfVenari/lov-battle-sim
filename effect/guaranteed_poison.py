from .effect import Effect
from .poison import Poison


class GuaranteedPoison(Effect):
    def __init__(self, messages):
        super().__init__(False, messages, None, 0)

    def description(self):
        return f"Guaranteed Poison on next basic attack."

    def on_apply(self, venari):
        super().on_apply(venari)
        self.messages.append(f"Guaranteed Poison!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'stackable': self.stackable,
            'duration': self.duration,
            'count': self.count,
            'description': self.description()
        }

    @classmethod
    def deserialize(cls, data, messages):
        return GuaranteedPoison(messages)