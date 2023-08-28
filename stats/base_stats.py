class BaseStats:
    def __init__(self, 
                 constitution=None,
                 strength=None,
                 intellect=None,
                 defence=None,
                 magic_resist=None,
                 passive_energy_gain=None,
                 basic_attack_energy_gain=None,
                 basic_attack_frequency=None,
                 basic_attack_damage=None,
                 passive_description=None,
                 ability_description=None,
                 swap_description=None):
        self.constitution = constitution
        self.strength = strength
        self.intellect = intellect
        self.defence = defence
        self.magic_resist = magic_resist
        self.passive_energy_gain = passive_energy_gain
        self.basic_attack_energy_gain = basic_attack_energy_gain
        self.basic_attack_frequency = basic_attack_frequency
        self.basic_attack_damage = basic_attack_damage
        self.passive_description = passive_description
        self.ability_description = ability_description
        self.swap_description = swap_description

    def serialize(self):
        return {
            'constitution': self.constitution,
            'strength': self.strength,
            'intellect': self.intellect,
            'defence': self.defence,
            'magic_resist': self.magic_resist,
            'passive_energy_gain': self.passive_energy_gain,
            'basic_attack_energy_gain': self.basic_attack_energy_gain,
            'basic_attack_frequency': self.basic_attack_frequency,
            'basic_attack_damage': self.basic_attack_damage,
            'passive_description': self.passive_description,
            'ability_description': self.ability_description,
            'swap_description': self.swap_description
        }

    @classmethod
    def deserialize(cls, data):
        return cls(constitution=data['constitution'],
                   strength=data['strength'],
                   intellect=data['intellect'],
                   defence=data['defence'],
                   magic_resist=data['magic_resist'],
                   passive_energy_gain=data['passive_energy_gain'],
                   basic_attack_energy_gain=data['basic_attack_energy_gain'],
                   basic_attack_frequency=data['basic_attack_frequency'],
                   basic_attack_damage=data['basic_attack_damage'],
                   passive_description=data['passive_description'],
                   ability_description=data['ability_description'],
                   swap_description=data['swap_description'])
