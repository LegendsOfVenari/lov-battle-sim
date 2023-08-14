from .effect import Effect


class Armor(Effect):
    def __init__(self):
        super().__init__(None)
        self.defense_boost = 0
        self.magic_resist_boost = 0

    def on_apply(self, venari):
        super().on_apply(venari)
        """Increase DEF and MAGIC RESIST by 50%."""
        self.defense_boost = 0.5 * venari.defense
        self.magic_resist_boost = 0.5 * venari.magic_resist

        venari.defense += self.defense_boost
        venari.magic_resist += self.magic_resist_boost

    def on_remove(self, venari):
        """Revert the DEF and MAGIC RESIST buff."""
        venari.defense -= self.defense_boost
        venari.magic_resist -= self.magic_resist_boost

    def description(self):
        """Override the description method for a more detailed description."""
        return f"Armor buff active, {self.count} stacks"

    def on_damage_received(self, venari, damage):
        self.remove_stack(venari)
        print(f"{venari.name} lost an Armor stack!")
