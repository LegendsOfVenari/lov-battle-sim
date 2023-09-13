from .stackable_effect import StackableEffect


class ArmyOfOne(StackableEffect):
    def __init__(self,
                 messages,
                 count=0):
        super().__init__(messages, None, None, count, False, True)
        self.effect_id = "army_of_one"

    def description(self):
        return f"Army of One ({self.count} Stacks, gaining {self.count} AD and AP)"

    def on_apply(self, venari):
        super().on_apply(venari)

        venari.battle_stats.attack_damage += 1
        venari.battle_stats.ability_power += 1

    def buffed_barrage(self, venari):
        venari.battle_stats.attack_damage += self.count * 0.2
        venari.battle_stats.ability_power += self.count * 0.2
        self.count *= 1.2

    def working_colony(self, venari):
        self.count += 2

    def on_ally_basic_attack(self, venari):
        self.on_apply(venari)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'count': self.count,
            'is_permanent': self.is_permanent
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return ArmyOfOne(messages,
                         data["count"])
