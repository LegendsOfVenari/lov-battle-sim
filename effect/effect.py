class Effect:
    def __init__(self, duration):
        self.duration = duration
        self.expired = False
        self.stackable = True
        self.count = 0

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each effect should have its own description method.")

    def on_tick(self, venari):
        """What the effect does on each tick."""
        pass

    def on_apply(self, venari):
        self.count += 1
        """What happens when the effect is first applied."""
        pass

    def on_remove(self, venari):
        """What happens when the effect is removed or expires."""
        pass

    def on_damage_received(self, venari, damage):
        """Placeholder for actions to be taken when the Venari with this effect receives damage.
        This can be overridden by subclasses as needed.
        """
        pass

    def stack(self):
        self.count += 1

    def remove_stack(self, venari):
        self.count -= 1
            
        # If no more counts, remove the effect
        if self.count == 0:
            venari.active_effects.remove(self)

    def tick(self):
        """Reduces the duration of the effect by one tick and checks if it's expired."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                self.expired = True