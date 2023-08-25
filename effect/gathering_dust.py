from .stackable_effect import StackableEffect


class GatheringDust(StackableEffect):
    def __init__(self,
                 messages,
                 count=0):
        super().__init__(messages, None, None, count, False, True)
        self.effect_id = "gathering_dust"

    def description(self):
        return f"Gathering Dust ({self.count} Stacks)"

    def on_apply(self, venari):
        super().on_apply(venari)
        self.count = min(5, self.count)

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'count': self.count
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return GatheringDust(messages,
                             data["count"])