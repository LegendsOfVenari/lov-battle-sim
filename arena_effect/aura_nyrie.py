from .aura import Aura


class AuraNyrie(Aura):
    def __init__(self, messages, duration=None, heal_tick=0):
        super().__init__(messages, duration)
        self.heal_amount = heal_tick

    def on_tick(self, venari):
        super().on_tick(venari)
        venari.heal(self.heal_tick)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'heal_amount': self.heal_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return AuraNyrie(messages,
                        data["duration"],
                        data["heal_amount"])