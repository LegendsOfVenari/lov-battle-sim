from .effect import Effect


class AttackDamageBuff(Effect):
    EFFECT_ID = "attack_damage_buff"

    def __init__(self, boost_amount, messages):
        super().__init__(messages, None)
        self.boost_amount = boost_amount

    def on_apply(self, venari):
        super().on_apply(venari)
        """Increase the attack damage by the specified amount."""
        venari.battle_stats.attack_damage += self.boost_amount

    def on_remove(self, venari):
        """Revert the attack damage boost."""
        venari.battle_stats.attack_damage -= self.boost_amount

    def description(self):
        return f"Increased Attack Damage by {self.boost_amount}."

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'boost_amount': self.boost_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return AttackDamageBuff(data["boost_amount"], messages)
