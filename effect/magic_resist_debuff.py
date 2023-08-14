from .effect import Effect


class MagicResistDebuff(Effect):
    def __init__(self, reduction_percent=10, duration=4):
        super().__init__(duration)
        # Convert the percentage to a factor
        self.reduction_factor = 1 - reduction_percent / 100

    def description(self):
        reduction_percentage = round(100 * (1 - self.reduction_factor), 1)
        return f"Magic Resist Debuff (-{reduction_percentage}%, {self.duration} ticks)"

    def on_apply(self, venari):
        # Reduce magic resist by the specified percentage
        venari.magic_resist *= self.reduction_factor

    def on_remove(self, venari):
        # Restore the magic resist
        venari.magic_resist /= self.reduction_factor
