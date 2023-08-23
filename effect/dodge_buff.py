from .effect import Effect


class DodgeBuff(Effect):

    def __init__(self, boost_amount, messages, duration, expired=False):
        super().__init__(messages, duration, expired)
        self.boost_amount = boost_amount
        self.effect_id = "dodge_buff"

    def on_apply(self, venari):
        super().on_apply(venari)
        """Increase the attack damage by the specified amount."""
        venari.battle_stats.dodge_chance += self.boost_amount

    def on_remove(self, venari):
        """Revert the attack damage boost."""
        venari.battle_stats.dodge_chance -= self.boost_amount

    def description(self):
        return f"{self.boost_amount}% Dodge [{self.duration} ticks]"

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'boost_amount': self.boost_amount,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return DodgeBuff(data["boost_amount"],
                         messages,
                         data["duration"],
                         data["expired"])
