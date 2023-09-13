from .stackable_effect import Effect
from config import DamageType

class MoonlitHuntMark(Effect):
    def __init__(self,
                 messages,
                 expired=False):
        super().__init__(messages, 12, expired, False)
        self.effect_id = "moonlit_hunt_mark"

    def description(self):
        return f"Moonlit Hunt Mark {self.duration} Duration"

    def modify_damage(self, venari, damage):
        return damage * 1.1

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return MoonlitHuntMark(messages,
                               data["expired"])
