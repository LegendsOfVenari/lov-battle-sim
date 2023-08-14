from .effect import Effect


class DefenceDebuff(Effect):
    def __init__(self, reduction_percent=10, duration=4):
        super().__init__(duration)
        # Convert the percentage to a factor
        self.reduction_factor = 1 - reduction_percent / 100

    def description(self):
        reduction_percentage = round(100 * (1 - self.reduction_factor), 1)
        return f"Defence Debuff (-{reduction_percentage}%, {self.duration} ticks)"

    def on_apply(self, venari):
        # Reduce defence (armor) by the specified percentage
        venari.defense *= self.reduction_factor

    def on_remove(self, venari):
        # Restore the defence (armor)
        venari.defense /= self.reduction_factor