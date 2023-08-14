from .effect import Effect

class Stagger(Effect):
    def __init__(self):
        super().__init__(1)  # Stagger effect lasts for 1 tick (i.e., it affects the next action)

    def description(self):
        return f"Staggers the next basic attack."