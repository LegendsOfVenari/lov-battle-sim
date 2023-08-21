from .stackable_effect import StackableEffect


class Armor(StackableEffect):
    EFFECT_ID = "armor"

    def __init__(self, messages, defense_boost=0, magic_resist_boost=0, count=0):
        super().__init__(messages, None, count)
        self.defense_boost = defense_boost
        self.magic_resist_boost = magic_resist_boost

    def on_apply(self, venari):
        super().on_apply(venari)
        """Increase DEF and MAGIC RESIST by 50%."""
        self.defense_boost = 0.5 * venari.battle_stats.defense
        self.magic_resist_boost = 0.5 * venari.battle_stats.magic_resist

        venari.battle_stats.defense += self.defense_boost
        venari.battle_stats.magic_resist += self.magic_resist_boost

        self.messages.append(f"{venari.name} gained {self.defense_boost} defense and {self.magic_resist_boost} magic resist!")

    def on_remove(self, venari):
        """Revert the DEF and MAGIC RESIST buff."""
        venari.battle_stats.defense -= self.defense_boost
        venari.battle_stats.magic_resist -= self.magic_resist_boost

    def description(self):
        return f"Armor buff active, {self.count} stacks, currently gaining {self.defense_boost} Defense and {self.magic_resist_boost}"

    def on_damage_received(self, venari, damage):
        if damage > 0:
            self.remove_stack(venari)
            self.messages.append(f"{venari.name} lost an Armor stack!")

    def stack(self):
        super().stack()
        self.messages.append(f"{self.count} Armor stacks!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'duration': self.duration,
            'count': self.count,
            'description': self.description(),
            'defense_boost': self.defense_boost,
            'magic_resist_boost': self.magic_resist_boost
        }

    @classmethod
    def deserialize(cls, data, messages):
        return Armor(messages, data["defense_boost"], data["magic_resist_boost"], data["count"])
