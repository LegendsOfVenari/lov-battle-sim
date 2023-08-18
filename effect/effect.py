import importlib

class Effect:
    def __init__(self, stackable, messages, duration=None, count=0):
        self.stackable = stackable
        self.messages = messages
        self.duration = duration
        self.count = count

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each effect should have its own description method.")

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                self.remove(venari)
        pass

    def on_apply(self, venari):
        if self.stackable:
            self.stack()
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

    def modify_basic_attack(self, venari, target):
        """Returns a boolean indicating if the basic attack should proceed."""
        return True

    def remove_stack(self, venari):
        self.count -= 1

        # If no more counts, remove the effect
        if self.count <= 0:
            venari.battle_handler.active_effects.remove(self)
            self.messages.append(f"{venari.name}'s effect has expired.")

    def remove(self, venari):
        self.on_remove(venari)
        venari.battle_handler.active_effects.remove(self)
        self.messages.append(f"{venari.name}'s effect has expired.")

    def serialize(self):
        raise NotImplementedError("Each effect should have its own serialization method.")

    @classmethod
    def deserialize(cls, data, messages):
        print(cls.__name__, data)

        name = data['name']
        module = importlib.import_module("effect")
        effect_class = getattr(module, name)

        return effect_class.deserialize(data, messages)
