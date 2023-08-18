from enum import Enum

aharas_base_stats = {
    "Constitution": 70,
    "Attack Damage": 82,
    "Ability Power": 68,
    "Defence": 57,
    "Magic Resist": 64,
    "Energy Gain Passively": 10,
    "Basic Attack Energy Gain": 14,
    "Basic Attack Frequency": 3,
    "Basic Attack Damage": 35
}

akulaw_base_stats = {
    "Constitution": 89,
    "Attack Damage": 89,
    "Ability Power": 70,
    "Defence": 86,
    "Magic Resist": 88,
    "Energy Gain Passively": 12,
    "Basic Attack Energy Gain": 16,
    "Basic Attack Frequency": 5,
    "Basic Attack Damage": 45
}

algala_base_stats = {
    "Constitution": 98,
    "Attack Damage": 104,
    "Ability Power": 34,
    "Defence": 82,
    "Magic Resist": 60,
    "Energy Gain Passively": 8,
    "Basic Attack Energy Gain": 10,
    "Basic Attack Frequency": 5,
    "Basic Attack Damage": 35
}

venari_base_stats_map = {
    'Aharas': aharas_base_stats,
    'Akulaw': akulaw_base_stats,
    'Algala': algala_base_stats
}


class DamageType(Enum):
    AD = "ad"
    AP = "ap"
    TRUE_DAMAGE = "true_damage"
