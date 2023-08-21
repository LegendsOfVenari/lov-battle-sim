import importlib


class Effect:

    def __init__(self, messages, duration=None):
        self.messages = messages
        self.duration = duration
        self.id = "none"

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each effect should have its own description method.")

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                self.remove(venari)

    def on_apply(self, venari):
        """What happens when the effect is first applied."""
        pass

    def on_remove(self, venari):
        """What happens when the effect is removed or expires."""
        pass

    def on_damage_received(self, venari, damage):
        """Placeholder for actions to be taken when the Venari with this effect receives damage."""
        pass

    def modify_basic_attack(self, venari, target):
        """Returns a boolean indicating if the basic attack should proceed."""
        return True

    def remove(self, venari):
        self.on_remove(venari)
        venari.battle_handler.remove_effect(self.get_id())
        self.messages.append(f"{venari.name}'s effect has expired.")

    def serialize(self):
        raise NotImplementedError("Each effect should have its own serialization method.")

    @classmethod
    def deserialize(cls, data, messages):

        name = data['name']
        module = importlib.import_module("effect")
        effect_class = getattr(module, name)

        return effect_class.deserialize(data, messages)

    @classmethod
    def get_id(cls):
        return None
