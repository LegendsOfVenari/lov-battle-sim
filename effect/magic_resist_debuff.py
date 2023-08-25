from .effect import Effect


class MagicResistDebuff(Effect):

    def __init__(self,
                 messages,
                 duration,
                 reduction_percent,
                 reduction_amount=0,
                 expired=False,
                 is_permanent=False):
        super().__init__(messages, duration, expired)
        # Convert the percentage to a factor
        self.reduction_percent = reduction_percent
        self.reduction_amount = reduction_amount
        self.effect_id = "magic_resist_debuff"

    def description(self):
        return f"MR Debuff({self.duration}) [{self.reduction_percent}%, -{round(self.reduction_amount, 2)} MR]"

    def on_apply(self, venari):
        super().on_apply(venari)
        # Reduce magic resist by the specified percentage
        reduction_factor = self.reduction_percent / 100
        self.reduction_amount = venari.battle_stats.magic_resist * reduction_factor
        venari.battle_stats.magic_resist = max(venari.battle_stats.magic_resist - self.reduction_amount, 0)


    def on_remove(self, venari):
        # Restore the magic resist
        venari.battle_stats.magic_resist += self.reduction_amount

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'reduction_percent': self.reduction_percent,
            'reduction_amount': self.reduction_amount,
            'expired': self.expired,
            'is_permanent': self.is_permanent
        }

    @classmethod
    def deserialize(cls, data, messages):
        return MagicResistDebuff(messages,
                                 data["duration"],
                                 data["reduction_percent"],
                                 data["reduction_amount"],
                                 data["expired"],
                                 data["is_permanent"])
