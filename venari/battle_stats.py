class BattleStats:
    def __init__(self, base_stats=None, level=None, hp=None,
                 constitution=None, attack_damage=None,
                 ability_power=None, defense=None,
                 magic_resist=None, accuracy=None):
        print(type(level))

        # If specific stats values are provided (deserialization scenario), use them.
        if hp is not None:
            self.hp = hp
            self.constitution = constitution
            self.attack_damage = attack_damage
            self.ability_power = ability_power
            self.defense = defense
            self.magic_resist = magic_resist
            self.accuracy = accuracy
        # Else, if base stats and level are provided, compute them.
        elif base_stats is not None and level is not None:
            self.constitution = ((2 * base_stats["Constitution"] * (level + 4)) / 100)
            self.attack_damage = ((2 * base_stats["Attack Damage"] * (level + 4)) / 100)
            self.ability_power = ((2 * base_stats["Ability Power"] * (level + 4)) / 100)
            self.defense = ((2 * base_stats["Defence"] * (level + 4)) / 100)
            self.magic_resist = ((2 * base_stats["Magic Resist"] * (level + 4)) / 100)
            self.hp = 10 * level + self.constitution * 15 + 100
            self.accuracy = 100
        # If neither set of parameters are provided, raise an error.
        else:
            raise ValueError("Must provide either base stats and level, or individual stat values.")

    def serialize(self):
        return {
            'hp': self.hp,
            'constitution': self.constitution,
            'attack_damage': self.attack_damage,
            'ability_power': self.ability_power,
            'defense': self.defense,
            'magic_resist': self.magic_resist,
            'accuracy': self.accuracy
        }

    @classmethod
    def deserialize(cls, data):
        return cls(hp=data['hp'],
                   constitution=data['constitution'],
                   attack_damage=data['attack_damage'],
                   ability_power=data['ability_power'],
                   defense=data['defense'],
                   magic_resist=data['magic_resist'],
                   accuracy=data['accuracy'])
