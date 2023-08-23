from .effect import Effect


class AttackDamageBuff(Effect):
    def __init__(self, boost_amount, messages, expired=False):
        super().__init__(messages, None, expired)
        self.boost_amount = boost_amount
        self.effect_id = "attack_damage_buff"

    def on_apply(self, venari):
        super().on_apply(venari)
        """Increase the attack damage by the specified amount."""
        venari.battle_stats.attack_damage += self.boost_amount

    def on_remove(self, venari):
        """Revert the attack damage boost."""
        venari.battle_stats.attack_damage -= self.boost_amount

    def description(self):
        return f"Attack Damage Buff ({self.boost_amount}) AD."

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
        return AttackDamageBuff(data["boost_amount"],
                                messages,
                                data["expired"])
