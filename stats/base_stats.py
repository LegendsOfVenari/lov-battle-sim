class BaseStats:
    def __init__(self, 
                 constitution=None,
                 attack_damage=None,
                 ability_power=None,
                 defence=None,
                 magic_resist=None,
                 passive_energy_gain=None,
                 basic_attack_energy_gain=None,
                 basic_attack_frequency=None,
                 basic_attack_damage=None):
        self.constitution = constitution
        self.attack_damage = attack_damage
        self.ability_power = ability_power
        self.defence = defence
        self.magic_resist = magic_resist
        self.passive_energy_gain = passive_energy_gain
        self.basic_attack_energy_gain = basic_attack_energy_gain
        self.basic_attack_frequency = basic_attack_frequency
        self.basic_attack_damage = basic_attack_damage

    def serialize(self):
        return {
            'constitution': self.constitution,
            'attack_damage': self.attack_damage,
            'ability_power': self.ability_power,
            'defence': self.defence,
            'magic_resist': self.magic_resist,
            'passive_energy_gain': self.passive_energy_gain,
            'basic_attack_energy_gain': self.basic_attack_energy_gain,
            'basic_attack_frequency': self.basic_attack_frequency,
            'basic_attack_damage': self.basic_attack_damage
        }

    @classmethod
    def deserialize(cls, data):
        return cls(constitution=data['constitution'],
                   attack_damage=data['attack_damage'],
                   ability_power=data['ability_power'],
                   defence=data['defence'],
                   magic_resist=data['magic_resist'],
                   passive_energy_gain=data['passive_energy_gain'],
                   basic_attack_energy_gain=data['basic_attack_energy_gain'],
                   basic_attack_frequency=data['basic_attack_frequency'],
                   basic_attack_damage=data['basic_attack_damage'])
