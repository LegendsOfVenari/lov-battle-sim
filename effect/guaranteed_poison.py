from .effect import Effect
from .poison import Poison


class GuaranteedPoison(Effect):
    EFFECT_ID = "guaranteed_poison"

    def __init__(self, messages, duration=6):
        super().__init__(messages)

    def description(self):
        return f"The next basic attack in the next {self.duration} ticks will apply poison."

    def on_apply(self, venari):
        super().on_apply(venari)
        self.messages.append(f"Guaranteed Poison activated!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration
        }

    @classmethod
    def deserialize(cls, data, messages):
        return GuaranteedPoison(messages, data["duration"])