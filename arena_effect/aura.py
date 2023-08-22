from .arena_effect import ArenaEffect


class Aura(ArenaEffect):
    def __init__(self, messages, duration=None):
        super().__init__(messages, duration)
