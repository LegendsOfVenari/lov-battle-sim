from enum import Enum
from stats import BaseStats

aharas_base_stats = BaseStats(
    constitution=70,
    attack_damage=82,
    ability_power=68,
    defence=57,
    magic_resist=64,
    passive_energy_gain=10,
    basic_attack_energy_gain=14,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

akulaw_base_stats = BaseStats(
    constitution=89,
    attack_damage=89,
    ability_power=70,
    defence=86,
    magic_resist=88,
    passive_energy_gain=12,
    basic_attack_energy_gain=16,
    basic_attack_frequency=5,
    basic_attack_damage=45
)

algala_base_stats = BaseStats(
    constitution=98,
    attack_damage=104,
    ability_power=34,
    defence=82,
    magic_resist=60,
    passive_energy_gain=8,
    basic_attack_energy_gain=10,
    basic_attack_frequency=5,
    basic_attack_damage=35
)

meeka_base_stats = BaseStats(
    constitution=95,
    attack_damage=70,
    ability_power=64,
    defence=64,
    magic_resist=65,
    passive_energy_gain=10,
    basic_attack_energy_gain=14,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

venari_base_stats_map = {
    'Aharas': aharas_base_stats,
    'Akulaw': akulaw_base_stats,
    'Algala': algala_base_stats,
    'Meeka': meeka_base_stats
}


class DamageType(Enum):
    AD = "ad"
    AP = "ap"
    TRUE_DAMAGE = "true_damage"
