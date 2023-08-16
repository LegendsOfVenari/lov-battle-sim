from .effect import Effect


class DefenceDebuff(Effect):
    def __init__(self, reduction_percent, duration):
        super().__init__(False, duration, 0)
        # Convert the percentage to a factor
        self.reduction_factor = reduction_percent / 100
        self.reduction_amount = 0

    def description(self):
        reduction_percentage = round(100 * (1 - self.reduction_factor), 1)
        return f"Defence Debuff (-{reduction_percentage}%, {self.duration} ticks)"

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)
        # Reduce defence (armor) by the specified percentage
        reduction_amount = venari.defense * self.reduction_factor
        venari.defense = max(venari.defense - reduction_amount, 0)
        messages.append(f"{venari.name}'s defence was reduced by {round(reduction_amount, 1)}")

    def on_remove(self, venari, messages):
        # Restore the defence (armor)
        venari.defense += self.reduction_amount
        messages.append(f"{venari.name}'s defence was restored by {round(self.reduction_amount, 1)}")
