from .stackable_effect import StackableEffect


class HaresAcceleration(StackableEffect):
    def __init__(self,
                 messages,
                 count=0):
        super().__init__(messages, None, None, count, False, True, 2)
        self.effect_id = "hares_acceleration"

    def description(self):
        return f"Hare Acceleration ({self.count} Stacks)"

    def on_tick(self, venari):
        # recalculate damage multiplier every tick
        venari.battle_stats.attack_speed -= self.count
        venari.battle_stats.attack_speed += self.count

    def on_stack_applied(self, venari):
        venari.battle_stats.attack_speed += 1

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'count': self.count
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return HaresAcceleration(messages,
                                 data["count"])
