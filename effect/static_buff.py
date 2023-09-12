from .effect import Effect

class StaticBuff(Effect):
    def __init__(self,
                 messages,
                 duration,
                 increase_amount,  # Changed from increase_percent
                 stat_to_change,
                 expired=False):
        super().__init__(messages, duration, expired)
        self.increase_amount = increase_amount  # Changed from increase_percent
        self.stat_to_change = stat_to_change
        self.effect_id = f"{stat_to_change}_static_buff"  # Changed from percent to static

    def description(self):
        return (f"{self.stat_to_change.capitalize()} Buff({self.duration}) "
                f"[+{self.increase_amount} {self.stat_to_change.upper()}]")  # Changed from percent to static amount

    def on_apply(self, venari):
        super().on_apply(venari)
        current_stat = getattr(venari.battle_stats, self.stat_to_change)
        new_stat = current_stat + self.increase_amount  # Changed from percent to static amount
        setattr(venari.battle_stats, self.stat_to_change, new_stat)

    def on_remove(self, venari):
        super().on_remove(venari)
        current_stat = getattr(venari.battle_stats, self.stat_to_change)
        new_stat = current_stat - self.increase_amount  # Changed from percent to static amount
        setattr(venari.battle_stats, self.stat_to_change, new_stat)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'increase_amount': self.increase_amount,  # Changed from increase_percent
            'stat_to_change': self.stat_to_change,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return StaticBuff(messages,
                          data["duration"],
                          data["increase_amount"],  # Changed from increase_percent
                          data["stat_to_change"],
                          data["expired"])
