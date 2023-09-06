import importlib


class Effect:

    def __init__(self,
                 messages,
                 duration=None,
                 expired=False,
                 is_permanent=False):
        self.messages = messages
        self.duration = duration
        self.effect_id = "none"
        self.expired = expired
        self.is_permanent = is_permanent

    def description(self):
        """Returns a human-readable description of the effect."""
        raise NotImplementedError("Each effect should have its own description method.")

    # Callback methods

    def on_tick(self, venari):
        """What the effect does on each tick."""
        if self.duration:
            self.duration -= 1
            if self.duration <= 0:
                self.remove()

    def on_apply(self, venari):
        """What happens when the effect is first applied."""
        pass

    def on_remove(self, venari):
        self.messages.append(f"{venari.name}'s {self.effect_id} effect has expired.")
        """What happens when the effect is removed or expires."""
        pass

    def on_damage_received(self, venari, damage):
        """Placeholder for actions to be taken when the Venari with this effect receives damage."""
        pass

    def on_ally_defeated(self):
        """Placeholder for actions to be taken when an ally is defeated."""
        pass

    def on_ally_basic_attack(self, venari):
        """Placeholder for actions to be taken when an ally basic attacks."""
        pass

    # Utility methods

    def remove(self):
        self.expired = True

    def modify_auto_attack(self, venari):
        """Returns a boolean indicating if the basic attack should proceed."""
        return False

    def modify_swap(self):
        """Returns a boolean indicating if the swap should proceed."""
        return False

    def modify_ability(self, venari):
        """Returns a boolean indicating if the ability should proceed."""
        return False

    # Serialization

    def serialize(self):
        raise NotImplementedError("Each effect should have its own serialization method.")

    @classmethod
    def deserialize(cls, data, messages):

        name = data['name']
        module = importlib.import_module("effect")
        effect_class = getattr(module, name)

        return effect_class.deserialize(data, messages)

