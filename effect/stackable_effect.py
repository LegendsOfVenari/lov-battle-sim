from .effect import Effect


class StackableEffect(Effect):
    def __init__(self,
                 messages,
                 initial_duration=None,
                 duration=None,
                 count=0,
                 expired=False,
                 is_permanent=False,
                 max_stacks=None):
        super().__init__(messages, duration, expired, is_permanent)
        self.count = count
        self.initial_duration = initial_duration
        self.max_stacks = max_stacks

    def on_stack_applied(self, venari):
        pass

    def stack(self, venari):
        if self.max_stacks is None or self.count < self.max_stacks:
            self.count += 1
            self.on_stack_applied(venari)

    def reset(self):
        self.count = 0

    def on_apply(self, venari):
        self.stack(venari)

    def remove_stack(self, venari):
        self.count -= 1
        # If no more counts, remove the effect
        if self.count <= 0:
            if not self.is_permanent:
                self.remove()

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                if self.count > 1:
                    self.count -= 1
                    self.duration = self.initial_duration
                else:
                    self.remove()
