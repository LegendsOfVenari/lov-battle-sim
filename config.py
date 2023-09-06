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
    basic_attack_damage=35,
    passive_description="Basic Attacks refresh the duration of all [Poison] effects",
    ability_description="Consume all stacks of [Poison] on the target dealing 3x the remaining amount of damage that the stacks of [Poison] would have done.",
    swap_description="Apply 1 stack of [Poison] to Point Venari."
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
    basic_attack_damage=35,
    passive_description="Gain [Armor] and [10 AD] for every 30% missing health",
    ability_description="Charges recklessly at the opposing Venari, dealing [75 AD] to both the target and self. Self damage is ignored if the Algala has at least 1 Armor stack.",
    swap_description="Algala enters the arena smashing the ground with it’s head applying [Stun] to both the Enemy Point Venari and Algala"
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
    basic_attack_damage=35,
    passive_description="If an enemy attack misses, Meeka's next basic attack within the next 2 ticks deals a bonus [30 AD].",
    ability_description="Meeka throws sand at the enemy Point Venari, Accuracy Debuff 50% - 6 ticks duration",
    swap_description="Deal [20 AD] upon swapping in. Accuracy Debuff 20% - 3 tick duration"
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
    basic_attack_damage=35,
    passive_description="Every 3rd basic attack generates 5 bonus energy for any allied Bench Venari.",
    ability_description="Creates a healing [Aura] that lasts on the allied Point Position. The [Ready to Help] aura heals [30 AP] per tick and grants a [-1 Tick Attack Speed] buff that lasts 6 ticks.",
    swap_description="Reduce the other Bench Venari’s swap cooldown by 2 ticks."
)

vespille_base_stats = BaseStats(
    constitution=91,
    strength=44,
    intellect=70,
    defence=40,
    magic_resist=75,
    passive_energy_gain=10,
    basic_attack_energy_gain=16,
    basic_attack_frequency=3,
    basic_attack_damage=35,
    passive_description="Gain a stack of [Gathering Dust] every auto attack. Max 5 stacks. For each stack of [Gathering Dust], gain 10% dodge chance for Vespille.",
    ability_description="Expel all stacks of [Gathering Dust] and create an Aura that grants [10% * Gathering Dust Stacks expelled] Dodge Chance for 12 ticks.",
    swap_description="Gain 50% dodge rate for 3 ticks upon swapping in."
)

valtri_base_stats = BaseStats(
    constitution=76,
    strength=83,
    intellect=71,
    defence=90,
    magic_resist=85,
    passive_energy_gain=12,
    basic_attack_energy_gain=16,
    basic_attack_frequency=4,
    basic_attack_damage=35,
    passive_description="Valtri gains a [75% AD] buff for each defeated ally venari, maxing at 150% AD.",
    ability_description="Valtri howls, [Marking] all opposing Venari for 12 ticks. This [Moonlit Hunt Mark] is unremovable and lasts its entire duration. (This is basically giving Valtri a unique, stronger Mark that applies to all enemies, granting Valtri’s team an offensive period against the opponent)",
    swap_description="Upon swapping in, the first attack against Valtri will always miss."
)

antello_base_stats = BaseStats(
    constitution=75,
    strength=44,
    intellect=97,
    defence=68,
    magic_resist=74,
    passive_energy_gain=10,
    basic_attack_energy_gain=20,
    basic_attack_frequency=3,
    basic_attack_damage=35,
    passive_description="Whenever Antello takes damage, heals a random wounded Venari on the allied Bench by [20 AP].",
    ability_description="Apply an [Aura] on your field that heals any Venari in the Point Position by [30 AP] every tick. Aura lasts for 12 ticks.",
    swap_description="Antello heals 30% of its maximum HP over the next 8 ticks."
)

folicri_base_stats = BaseStats(
    constitution=66,
    strength=35,
    intellect=65,
    defence=42,
    magic_resist=45,
    passive_energy_gain=16,
    basic_attack_energy_gain=14,
    basic_attack_frequency=3,
    basic_attack_damage=35
)

eurici_base_stats = BaseStats(
    constitution=101,
    strength=52,
    intellect=42,
    defence=72,
    magic_resist=60,
    passive_energy_gain=16,
    basic_attack_energy_gain=10,
    basic_attack_frequency=5,
    basic_attack_damage=35,
    passive_description="Gain 1 [Armor] for each enemy Venari is [Webbed].",
    ability_description="Deal 15 AP damage. [Web] all enemy Venari for 3 Ticks.",
    swap_description="Deal [10] AP damage and [Web] Point Venari for 8 Ticks. If Venari is already [Poisoned] or [Stunned], gain 8 points to energy bar."
)

laticus_base_stats = BaseStats(
    constitution=70,
    strength=43,
    intellect=30,
    defence=57,
    magic_resist=53,
    passive_energy_gain=12,
    basic_attack_energy_gain=10,
    basic_attack_frequency=3,
    basic_attack_damage=35,
    passive_description="Gain [1 AD] and [1 AP] for every Basic Attack done by your team.",
    ability_description="Double the amount of Stacks that Laticus currently has.",
    swap_description="Multi-attack 5 times (5 AP damage) after swapping."
)

venari_base_stats_map = {
    'Aharas': aharas_base_stats,
    'Akulaw': akulaw_base_stats,
    'Algala': algala_base_stats,
    'Meeka': meeka_base_stats,
    'Nyrie': nyrie_base_stats,
    'Vespille': vespille_base_stats,
    'Valtri': valtri_base_stats,
    'Antello': antello_base_stats,
    'Folicri': folicri_base_stats,
    'Eurici': eurici_base_stats,
    'Laticus': laticus_base_stats
}

class DamageType(Enum):
    AD = "ad"
    AP = "ap"
    TRUE_DAMAGE = "true_damage"
