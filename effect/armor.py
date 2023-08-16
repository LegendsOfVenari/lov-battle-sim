from .effect import Effect


class Armor(Effect):
    def __init__(self, defense_boost=0, magic_resist_boost=0, count=0):
        super().__init__(True, None, count)
        self.defense_boost = defense_boost
        self.magic_resist_boost = magic_resist_boost

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)
        """Increase DEF and MAGIC RESIST by 50%."""
        self.defense_boost = 0.5 * venari.defense
        self.magic_resist_boost = 0.5 * venari.magic_resist

        venari.defense += self.defense_boost
        venari.magic_resist += self.magic_resist_boost

        messages.append(f"{venari.name} gained {self.defense_boost} defense and {self.magic_resist_boost} magic resist!")

    def on_remove(self, venari):
        """Revert the DEF and MAGIC RESIST buff."""
        venari.defense -= self.defense_boost
        venari.magic_resist -= self.magic_resist_boost

    def description(self):
        return f"Armor buff active, {self.count} stacks"

    def on_damage_received(self, venari, damage, messages):
        self.remove_stack(venari)
        messages.append(f"{venari.name} lost an Armor stack!")

    def stack(self, messages):
        super().stack(messages)
        messages.append(f"{self.count} Armor stacks!")
