import importlib


class ArenaEffect:
    def __init__(self,
                 messages,
                 duration=None,
                 expired=False):
        self.messages = messages
        self.duration = duration
        self.expired = expired
        self.arena_effect_id = "none"

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each arena effect should have its own description method.")

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                self.remove()

    # Callback methods

    def on_swap_in(self, venari):
        pass

    def on_remove(self, venari):
        """What happens when the effect is removed or expires."""
        pass

    # Utility methods

    def remove(self):
        self.messages.append(f"{self.arena_effect_id}'s effect is expiring.")
        self.expired = True

    def serialize(self):
        raise NotImplementedError("Each effect should have its own serialization method.")

    @classmethod
    def deserialize(cls, data, messages):

        name = data['name']
        module = importlib.import_module("arena_effect")
        effect_class = getattr(module, name)

        return effect_class.deserialize(data, messages)
