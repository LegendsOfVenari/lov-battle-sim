from .stackable_effect import StackableEffect


class Unique(StackableEffect):

    def __init__(self,
                 messages,
                 effect_id,
                 initial_duration,
                 duration,
                 count=0,
                 expired=False,
                 is_permanent=False,
                 max_stacks=None):
        super().__init__(
            messages,
            initial_duration,
            duration,
            count,
            expired,
            is_permanent,
            max_stacks
        )
        self.effect_id = effect_id

    def description(self):
        return f"Unique ({self.effect_id}): {self.count} stacks, ({self.duration} ticks)"

    def serialize(self):
        return {
            'effect_id': self.effect_id,
            'name': self.__class__.__name__,
            'description': self.description(),
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count,
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'max_stacks': self.max_stacks
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(f"{data}")
        return Unique(messages,
                      data["effect_id"],
                      data["initial_duration"],
                      data["duration"],
                      data["count"],
                      data["expired"],
                      data["is_permanent"],
                      data["max_stacks"])
