from .effect import Effect

class DefenceDebuff(Effect):
    def __init__(self, reduction_percent=10, duration=4):
        super().__init__(duration)
        self.reduction_factor = 1 - reduction_percent / 100  # Convert the percentage to a factor

    def description(self):
        reduction_percentage = round(100 * (1 - self.reduction_factor), 1)
        return f"Defence Debuff (-{reduction_percentage}%, {self.duration} ticks)"

    def on_apply(self, venari):
        venari.defense *= self.reduction_factor  # Reduce defence (armor) by the specified percentage

    def on_remove(self, venari):
        venari.defense /= self.reduction_factor  # Restore the defence (armor)