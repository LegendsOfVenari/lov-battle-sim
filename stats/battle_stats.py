class BattleStats:
    def __init__(self, base_stats=None, level=None, hp=None,
                 constitution=None, attack_damage=None,
                 ability_power=None, defense=None,
                 magic_resist=None, accuracy=None,
                 initial_hp=None, dodge_chance=None):
        if hp is not None:
            self.hp = hp
            self.constitution = constitution
            self.attack_damage = attack_damage
            self.ability_power = ability_power
            self.defense = defense
            self.magic_resist = magic_resist
            self.accuracy = accuracy
            self.initial_hp = initial_hp
            self.dodge_chance = dodge_chance
        elif base_stats is not None and level is not None:
            self.constitution = ((2 * base_stats.constitution * (level + 4)) / 100)
            self.attack_damage = ((2 * base_stats.strength * (level + 4)) / 100)
            self.ability_power = ((2 * base_stats.intellect * (level + 4)) / 100)
            self.defense = ((2 * base_stats.defence * (level + 4)) / 100)
            self.magic_resist = ((2 * base_stats.magic_resist * (level + 4)) / 100)
            self.hp = 10 * level + self.constitution * 15 + 100
            self.accuracy = 100
            self.initial_hp = self.hp
            self.dodge_chance = 0
        # If neither set of parameters are provided, raise an error.
        else:
            raise ValueError("Must provide either base stats and level, or individual stat values.")

    def hp_percentage(self):
        return self.hp / self.initial_hp

    def increase_dodge_chance(self, amount):
        self.dodge_chance += amount
        self.dodge_chance = min(self.dodge_chance, 100)

    def decrease_dodge_chance(self, amount):
        self.dodge_chance -= amount
        self.dodge_chance = max(self.dodge_chance, 0)

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
        return cls(hp=data['hp'],
                   constitution=data['constitution'],
                   attack_damage=data['attack_damage'],
                   ability_power=data['ability_power'],
                   defense=data['defense'],
                   magic_resist=data['magic_resist'],
                   accuracy=data['accuracy'],
                   initial_hp=data['initial_hp'],
                   dodge_chance=data['dodge_chance'])
