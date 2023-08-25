from .arena_effect import ArenaEffect


class Aura(ArenaEffect):
    def __init__(self, messages, duration=None, expired=False):
        super().__init__(messages, duration, expired)
