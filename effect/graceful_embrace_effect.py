from .effect import Effect
from config import graceful_embrace_bonus_magic_resist, graceful_embrace_bonus_ability_power


class GracefulEmbraceEffect(Effect):
    def __init__(self,
                 messages,
                 duration=1,
                 expired=False):
        super().__init__(messages, duration, expired, False)
        self.effect_id = "graceful_embrace_effect"

    def description(self):
        return f"Ready To Help: {self.duration} remaining"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Refresh Duration
        self.duration = 1
        venari.battle_stats.magic_resist += graceful_embrace_bonus_magic_resist
        venari.battle_stats.ability_power += graceful_embrace_bonus_ability_power

    def on_remove(self, venari):
        venari.battle_stats.magic_resist -= graceful_embrace_bonus_magic_resist
        venari.battle_stats.ability_power -= graceful_embrace_bonus_ability_power

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'duration': self.duration,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return GracefulEmbraceEffect(messages,
                                     data["duration"],
                                     data["expired"])
