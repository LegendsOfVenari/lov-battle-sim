from .effect import Effect

class Shield(Effect):

    def __init__(self, messages, shield_amount, duration=None, expired=False, is_permanent=False):
        super().__init__(messages, duration, expired)
        self.effect_id = "shield"
        self.shield_amount = shield_amount

    def description(self):
        return f"Shield ({self.shield_amount} for {self.duration} ticks)"

    def on_apply(self, venari):
        super().on_apply(venari)
        self.messages.append(f"{venari.name} received a shield of {self.shield_amount} strength!")

    def on_damage_received(self, venari, damage):
        damage_to_shield = min(self.shield_amount, damage)
        self.shield_amount -= damage_to_shield
        damage -= damage_to_shield
        if self.shield_amount <= 0:
            self.remove()
        return damage  # Remaining damage after shield absorption

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'shield_amount': self.shield_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Shield(messages,
                      data["shield_amount"],
                      data["duration"],
                      data["expired"],
                      data["is_permanent"])
