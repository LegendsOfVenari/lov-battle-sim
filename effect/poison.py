from .effect import Effect

class Poison(Effect):
    def __init__(self):
        super().__init__(6)  # Poison lasts for 6 ticks

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari):
        damage = 0.1 * venari.hp  # 10% of max HP
        venari.hp -= damage
        print(f"{venari.name} took {damage:.2f} poison damage!")

    def stack(self):
        super().stack()
        self.duration += 6
