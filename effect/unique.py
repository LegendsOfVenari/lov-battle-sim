from .stackable_effect import StackableEffect


class Unique(StackableEffect):

    def __init__(self, messages, effect_id, initial_duration, duration, count=0):
        super().__init__(messages, initial_duration, duration, count)
        self.effect_id = effect_id

    def description(self):
        return f"Unique ({self.id}): {self.count} stacks, ({self.duration} ticks)"

    def serialize(self):
        return {
            'effect_id': self.effect_id,
            'name': self.__class__.__name__,
            'description': self.description(),
            'initial_duration': self.initial_duration,
            'duration': self.duration,
            'count': self.count
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Unique(messages,
                      data["effect_id"],
                      data["initial_duration"],
                      data["duration"],
                      data["count"])

