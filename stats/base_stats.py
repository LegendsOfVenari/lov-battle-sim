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
                 basic_attack_damage=None):
        self.constitution = constitution
        self.strength = strength
        self.intellect = intellect
        self.defence = defence
        self.magic_resist = magic_resist
        self.passive_energy_gain = passive_energy_gain
        self.basic_attack_energy_gain = basic_attack_energy_gain
        self.basic_attack_frequency = basic_attack_frequency
        self.basic_attack_damage = basic_attack_damage

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
            'basic_attack_damage': self.basic_attack_damage
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
                   basic_attack_damage=data['basic_attack_damage'])
