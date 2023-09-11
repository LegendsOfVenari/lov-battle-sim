from .effect import Effect

class PercentStatBuff(Effect):
    def __init__(self,
                 messages,
                 duration,
                 increase_percent,
                 stat_to_change,
                 expired=False):
        super().__init__(messages, duration, expired)
        self.increase_percent = increase_percent
        self.stat_to_change = stat_to_change
        self.effect_id = f"{stat_to_change}_percent_buff"

    def description(self):
        return (f"{self.stat_to_change.capitalize()} Buff({self.duration}) "
                f"[{self.increase_percent}% {self.stat_to_change.upper()}]")

    def on_apply(self, venari):
        super().on_apply(venari)
        increase_factor = self.increase_percent / 100
        current_stat = getattr(venari.battle_stats, self.stat_to_change)
        increase_amount = current_stat * increase_factor
        new_stat = current_stat + increase_amount
        setattr(venari.battle_stats, self.stat_to_change, new_stat)

    def on_remove(self, venari):
        super().on_remove(venari)
        increase_factor = self.increase_percent / 100
        current_stat = getattr(venari.battle_stats, self.stat_to_change)
        increase_amount = current_stat * increase_factor
        new_stat = current_stat - increase_amount
        setattr(venari.battle_stats, self.stat_to_change, new_stat)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'description': self.description(),
            'increase_percent': self.increase_percent,
            'stat_to_change': self.stat_to_change,
            'expired': self.expired
        }

    @classmethod
    def deserialize(cls, data, messages):
        return PercentStatBuff(messages,
                               data["duration"],
                               data["increase_percent"],
                               data["stat_to_change"],
                               data["expired"])
