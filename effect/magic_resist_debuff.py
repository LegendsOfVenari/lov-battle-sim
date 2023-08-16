from .effect import Effect


class MagicResistDebuff(Effect):
    def __init__(self, reduction_percent, duration):
        super().__init__(False, duration, 0)
        # Convert the percentage to a factor
        self.reduction_factor = reduction_percent / 100
        self.reduction_amount = 0

    def description(self):
        reduction_percentage = round(100 * (1 - self.reduction_factor), 1)
        return f"Magic Resist Debuff (-{reduction_percentage}%, {self.duration} ticks)"

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)
        # Reduce magic resist by the specified percentage
        reduction_amount = venari.magic_resist * self.reduction_factor
        venari.magic_resist = max(venari.magic_resist - reduction_amount, 0)
        messages.append(f"{venari.name}'s magic resist was reduced by {round(reduction_amount, 1)}")


    def on_remove(self, venari, messages):
        # Restore the magic resist
        venari.magic_resist += self.reduction_amount
        messages.append(f"{venari.name}'s magic resist was restored by {round(self.reduction_amount, 1)}")
