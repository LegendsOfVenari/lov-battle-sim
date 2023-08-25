from .aura import Aura
from effect import DustCloudEffect

class DustCloudAura(Aura):
    def __init__(self, messages, dodge_chance, duration=12, expired=False):
        super().__init__(messages, duration)
        self.dodge_chance = dodge_chance
        self.arena_effect_id = "dust_cloud_aura"

    def on_tick(self, venari):
        super().on_tick(venari)
        # Apply Dust Cloud Effect
        venari.apply_effect(DustCloudEffect(self.messages, self.dodge_chance))

    def description(self):
        return f"Dust Cloud: Grants {self.dodge_chance}% dodge chance, {self.duration} seconds remaining"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired,
            'dodge_chance': self.dodge_chance
        }

    @classmethod
    def deserialize(cls, data, messages):
        return DustCloudAura(messages, data["dodge_chance"], data["duration"], data["expired"])
