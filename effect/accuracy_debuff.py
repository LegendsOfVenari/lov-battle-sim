from .effect import Effect


class AccuracyDebuff(Effect):

    def __init__(self, messages, duration, reduction_percent, reduction_amount=0, expired=False):
        super().__init__(messages, duration, expired)
        # Convert the percentage to a factor
        self.reduction_percent = reduction_percent
        self.reduction_amount = reduction_amount
        self.effect_id = "accuracy_debuff"

    def description(self):
        return f"Accuracy Debuff({self.duration}) [{self.reduction_percent}%, -{round(self.reduction_amount, 2)} Accuracy]"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Reduce defence (armor) by the specified percentage
        reduction_factor = self.reduction_percent / 100
        self.reduction_amount = venari.battle_stats.defense * reduction_factor
        venari.battle_stats.accuracy = max(venari.battle_stats.defense - self.reduction_amount, 0)
        self.messages.append(f"{venari.name}'s accuracy was reduced by {round(self.reduction_amount, 1)}")

    def on_remove(self, venari):
        # Restore the defence (armor)
        venari.battle_stats.defense += self.reduction_amount
        self.messages.append(f"{venari.name}'s accuracy was restored by {round(self.reduction_amount, 1)}")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'reduction_percent': self.reduction_percent,
            'reduction_amount': self.reduction_amount,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return AccuracyDebuff(messages,
                              data["duration"],
                              data["reduction_percent"],
                              data["reduction_amount"],
                              data["expired"],
)
