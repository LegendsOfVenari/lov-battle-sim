from .effect import Effect

class Stagger(Effect):
    def __init__(self, messages):
        super().__init__(False, messages, None, 0)

    def description(self):
        return f"Staggers the next basic attack."

    def on_apply(self, venari):
        super().on_apply(venari)

    def modify_basic_attack(self, venari, target):
        self.messages.append(f"{venari.name}({venari.level}) has been staggered")
        # remove the effect after it's triggered
        venari.battle_handler.remove_effect(Stagger)
        return False  # Basic attack does not proceed

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
        return Stagger(messages)