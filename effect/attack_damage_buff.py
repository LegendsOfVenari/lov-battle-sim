from .effect import Effect


class AttackDamageBuff(Effect):
    def __init__(self, boost_amount):
        super().__init__(False, None, 0)
        self.boost_amount = boost_amount
        self.applied_boost = 0

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)
        """Increase the attack damage by the specified amount."""
        venari.attack_damage += self.boost_amount
        self.applied_boost = self.boost_amount

    def on_remove(self, venari):
        """Revert the attack damage boost."""
        venari.attack_damage -= self.applied_boost

    def description(self):
        return f"Increased Attack Damage by {self.boost_amount}."
