from .effect import Effect


class StackableEffect(Effect):
    def __init__(self, messages, initial_duration=None, duration=None, count=0):
        super().__init__(messages, duration)
        self.count = count
        self.initial_duration = initial_duration

    def stack(self):
        self.count += 1

    def on_apply(self, venari):
        self.stack()

    def remove_stack(self, venari):
        self.count -= 1
        # If no more counts, remove the effect
        if self.count <= 0:
            self.remove(venari)

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                if self.count > 1:
                    self.count -= 1
                    self.duration = self.initial_duration
                else:
                    self.remove(venari)
