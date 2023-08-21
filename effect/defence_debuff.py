from .effect import Effect


class DefenceDebuff(Effect):
    EFFECT_ID = "defence_debuff"

    def __init__(self, messages, duration, reduction_percent, reduction_amount=0):
        super().__init__(messages, duration)
        # Convert the percentage to a factor
        self.reduction_percent = reduction_percent
        self.reduction_amount = reduction_amount

    def description(self):
        return f"Defence Debuff ({self.reduction_percent}%, {self.duration} ticks)"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Reduce defence (armor) by the specified percentage
        reduction_factor = self.reduction_percent / 100
        reduction_amount = venari.battle_stats.defense * reduction_factor
        venari.battle_stats.defense = max(venari.battle_stats.defense - reduction_amount, 0)
        self.messages.append(f"{venari.name}'s defence was reduced by {round(reduction_amount, 1)}")

    def on_remove(self, venari):
        # Restore the defence (armor)
        venari.battle_stats.defense += self.reduction_amount
        self.messages.append(f"{venari.name}'s defence was restored by {round(self.reduction_amount, 1)}")

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
        return DefenceDebuff(messages,
                             data["duration"],
                             data["reduction_percent"],
                             data["reduction_amount"])
