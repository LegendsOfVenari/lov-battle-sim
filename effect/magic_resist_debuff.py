from .effect import Effect


class MagicResistDebuff(Effect):

    def __init__(self, messages, duration, reduction_percent, reduction_amount=0):
        super().__init__(messages, duration)
        # Convert the percentage to a factor
        self.reduction_percent = reduction_percent
        self.reduction_amount = 0

    def description(self):
        return f"Magic Resist Debuff ({self.reduction_percent}%, {self.duration} ticks)"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Reduce magic resist by the specified percentage
        reduction_factor = self.reduction_percent / 100
        reduction_amount = venari.battle_stats.magic_resist * reduction_factor
        venari.battle_stats.magic_resist = max(venari.battle_stats.magic_resist - reduction_amount, 0)
        self.messages.append(f"{venari.name}'s magic resist was reduced by {round(reduction_amount, 1)}")


    def on_remove(self, venari):
        # Restore the magic resist
        venari.battle_stats.magic_resist += self.reduction_amount
        self.messages.append(f"{venari.name}'s magic resist was restored by {round(self.reduction_amount, 1)}")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'reduction_percent': self.reduction_percent,
            'reduction_amount': self.reduction_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return MagicResistDebuff(messages,
                                 data["duration"],
                                 data["reduction_percent"],
                                 data["reduction_amount"])

    @classmethod
    def get_id(cls):
        return "magic_resist_debuff"