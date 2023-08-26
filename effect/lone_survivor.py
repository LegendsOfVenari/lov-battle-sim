from .stackable_effect import StackableEffect


class LoneSurvivor(StackableEffect):
    def __init__(self,
                 messages,
                 count=0,
                 damage_buff=0):
        super().__init__(messages, None, None, count, False, True)
        self.effect_id = "lone_survivor"
        self.damage_buff = damage_buff

    def description(self):
        return f"Lone Survivor ({self.count} Stacks ({self.damage_buff}) AD)"

    def on_ally_defeated(self):
        self.count += 1

    def on_tick(self, venari):
        # recalculate damage multiplier every tick
        venari.battle_stats.attack_damage -= self.damage_buff
        buff = venari.battle_stats.attack_damage * 0.75 * (self.count - 1)
        venari.battle_stats.attack_damage += buff
        self.damage_buff = buff

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'count': self.count,
            'damage_buff': self.damage_buff
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return LoneSurvivor(messages,
                            data["count"],
                            data["damage_buff"])
