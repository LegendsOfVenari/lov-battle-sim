from .effect import Effect

class TrapEffect(Effect):

    def __init__(self,
                 messages,
                 duration=1,
                 expired=False):
        super().__init__(messages, duration, expired)
        self.effect_id = "stun"

    def description(self):
        return f"Stun, ({self.duration}) ticks"

    def on_apply(self, venari):
        super().on_apply(venari)

    def modify_auto_attack(self, venari):
        self.messages.append(f"{venari.name}({venari.level}) has been stunned")
        return True  # Basic attack does not proceed

    def modify_ability(self, venari):
        self.messages.append(f"{venari.name}({venari.level}) has been stunned")
        return True

    def modify_swap(self):
        self.messages.append("Trap has been triggered.")
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
        return TrapEffect(messages,
                        data["duration"],
                        data["expired"])
