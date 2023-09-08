from .effect import Effect
from config import graceful_embrace_bonus_magic_resist, graceful_embrace_bonus_ability_power


class GracefulEmbraceEffect(Effect):
    def __init__(self,
                 messages,
                 duration=1,
                 expired=False,
                 heal_amount=0):
        super().__init__(messages, duration, expired, False)
        self.effect_id = "graceful_embrace_effect"
        self.heal_amount = heal_amount

    def description(self):
        return f"Ready To Help: {round(self.heal_amount, 2)} HP, {self.duration} remaining"

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
            'expired': self.expired,
            'heal_amount': self.heal_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return GracefulEmbraceEffect(messages,
                                     data["duration"],
                                     data["expired"],
                                     data["heal_amount"])
