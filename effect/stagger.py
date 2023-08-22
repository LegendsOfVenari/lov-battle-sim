from .effect import Effect

class Stagger(Effect):

    def __init__(self, messages, duration=3):
        super().__init__(messages, duration)
        self.effect_id = "stagger"

    def description(self):
        return f"Stagger, {self.duration} ticks)"

    def on_apply(self, venari):
        super().on_apply(venari)

    def modify_basic_attack(self, venari, target):
        self.messages.append(f"{venari.name}({venari.level}) has been staggered")
        # remove the effect after it's triggered
        venari.battle_handler.remove_effect(Stagger.get_id())
        return False  # Basic attack does not proceed

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Stagger(messages,
                       data["duration"])

