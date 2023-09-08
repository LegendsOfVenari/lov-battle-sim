class BattleStats:
    def __init__(self, base_stats=None, level=None, **kwargs):
        if base_stats is not None and level is not None:
            self.set_stats_based_on_level(base_stats, level)
        elif kwargs:
            self.set_stats_directly(**kwargs)
        else:
            raise ValueError("Must provide either base stats and level, or individual stat values.")

    def set_stats_based_on_level(self, base_stats, level):
        self.constitution = ((2 * base_stats.constitution * (level + 4)) / 100)
        self.attack_damage = ((2 * base_stats.strength * (level + 4)) / 100)
        self.ability_power = ((2 * base_stats.intellect * (level + 4)) / 100)
        self.defense = ((2 * base_stats.defence * (level + 4)) / 100)
        self.magic_resist = ((2 * base_stats.magic_resist * (level + 4)) / 100)
        self.hp = 10 * level + self.constitution * 15 + 100
        self.accuracy = 100
        self.initial_hp = self.hp
        self.dodge_chance = 0

    def set_stats_directly(self, **kwargs):
        self.hp = kwargs.get('hp')
        self.constitution = kwargs.get('constitution')
        self.attack_damage = kwargs.get('attack_damage')
        self.ability_power = kwargs.get('ability_power')
        self.defense = kwargs.get('defense')
        self.magic_resist = kwargs.get('magic_resist')
        self.accuracy = kwargs.get('accuracy')
        self.initial_hp = kwargs.get('initial_hp')
        self.dodge_chance = kwargs.get('dodge_chance')

    @property
    def hp_percentage(self):
        return self.hp / self.initial_hp

    @property
    def dodge_chance(self):
        return self._dodge_chance

    @dodge_chance.setter
    def dodge_chance(self, value):
        self._dodge_chance = max(0, min(value, 100))

    @property
    def attack_damage(self):
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value):
        self._attack_damage = max(0, value)

    @property
    def magic_resist(self):
        return self._magic_resist

    @magic_resist.setter
    def magic_resist(self, value):
        self._magic_resist = max(0, value)

    @property
    def ability_power(self):
        return self._ability_power

    @ability_power.setter
    def ability_power(self, value):
        self._ability_power = max(0, value)

    def serialize(self):
        return {
            'hp': self.hp,
            'constitution': self.constitution,
            'attack_damage': self.attack_damage,
            'ability_power': self.ability_power,
            'defense': self.defense,
            'magic_resist': self.magic_resist,
            'accuracy': self.accuracy,
            'initial_hp': self.initial_hp,
            'dodge_chance': self.dodge_chance
        }

    @classmethod
    def deserialize(cls, data):
        return cls(**data)
