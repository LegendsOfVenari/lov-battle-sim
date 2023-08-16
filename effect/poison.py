from .effect import Effect

class Poison(Effect):
    def __init__(self):
        super().__init__(0)  # Poison lasts for 6 ticks per each stack

    def description(self):
        return f"Poison ({self.count}) stacks ({self.duration} ticks)"

    def on_tick(self, venari, messages):
        damage = 0.1 * venari.hp  # 10% of max HP
        venari.hp -= damage
        messages.append(f"{venari.name} took {damage:.2f} poison damage!")

    def stack(self, messages):
        super().stack(messages)
        self.duration += 6
