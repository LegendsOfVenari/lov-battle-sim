from .effect import Effect


class AttackDamageBuff(Effect):
    def __init__(self, boost_amount, messages):
        super().__init__(False, messages, None, 0)
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
            'stackable': self.stackable,
            'duration': self.duration,
            'count': self.count,
            'description': self.description(),
            'boost_amount': self.boost_amount
        }

    @classmethod
    def deserialize(cls, data, messages):
        return AttackDamageBuff(data["boost_amount"], messages)
