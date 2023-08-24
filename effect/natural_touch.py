from .stackable_effect import StackableEffect
from .armor import Armor


class NaturalTouch(StackableEffect):
    def __init__(self,
                 messages,
                 count=0,
                 is_permanent=True):
        super().__init__(messages, None, None, count, False, is_permanent)
        self.effect_id = "natural_touch"

    def description(self):
        return f"Natural Touch ({self.count} Stacks)"

    def on_apply(self, venari):
        super().on_apply(venari)

        if self.count == 3:
            self.count = 0
            ally_bench = venari.get_ally_bench()

            for ally in ally_bench:
                ally.gain_energy(5)
                self.messages.append(f"{ally.name} gained 5 energy!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'is_permanent': self.is_permanent,
            'count': self.count
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return NaturalTouch(messages,
                            data["is_permanent"],
                            data["count"])
