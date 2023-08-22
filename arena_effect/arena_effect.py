import importlib


class ArenaEffect:
    def __init__(self, messages, duration=None):
        self.messages = messages
        self.duration = duration
        self.arena_effect_id = "none"

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each effect should have its own description method.")

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1

    def on_swap_in(self, venari):
        pass

    def on_remove(self, venari):
        """What happens when the effect is removed or expires."""
        pass

    def remove(self, venari):
        venari.battle.remove_arena_effect(self.effect_id)
        self.messages.append(f"{self.arena_effect_id}'s effect has expired.")

    def serialize(self):
        raise NotImplementedError("Each effect should have its own serialization method.")

    @classmethod
    def deserialize(cls, data, messages):

        name = data['name']
        module = importlib.import_module("effect")
        effect_class = getattr(module, name)

        return effect_class.deserialize(data, messages)
