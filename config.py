from enum import Enum
from stats import BaseStats

aharas_base_stats = BaseStats(
    constitution=70,
    strength=82,
    intellect=68,
    defence=57,
    magic_resist=64,
    passive_energy_gain=10,
    basic_attack_energy_gain=14,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

akulaw_base_stats = BaseStats(
    constitution=89,
    strength=89,
    intellect=70,
    defence=86,
    magic_resist=88,
    passive_energy_gain=12,
    basic_attack_energy_gain=16,
    basic_attack_frequency=5,
    basic_attack_damage=45
)

algala_base_stats = BaseStats(
    constitution=98,
    strength=104,
    intellect=34,
    defence=82,
    magic_resist=60,
    passive_energy_gain=8,
    basic_attack_energy_gain=10,
    basic_attack_frequency=5,
    basic_attack_damage=35
)

meeka_base_stats = BaseStats(
    constitution=95,
    strength=70,
    intellect=64,
    defence=64,
    magic_resist=65,
    passive_energy_gain=10,
    basic_attack_energy_gain=14,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

nyrie_base_stats = BaseStats(
    constitution=42,
    strength=40,
    intellect=107,
    defence=71,
    magic_resist=105,
    passive_energy_gain=16,
    basic_attack_energy_gain=20,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

venari_base_stats_map = {
    'Aharas': aharas_base_stats,
    'Akulaw': akulaw_base_stats,
    'Algala': algala_base_stats,
    'Meeka': meeka_base_stats,
    'Nyrie': nyrie_base_stats
}

class DamageType(Enum):
    AD = "ad"
    AP = "ap"
    TRUE_DAMAGE = "true_damage"
