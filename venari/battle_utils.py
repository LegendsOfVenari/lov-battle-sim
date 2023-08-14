from enum import Enum

class DamageType(Enum):
    AD = "ad"
    AP = "ap"
    TRUE_DAMAGE = "true_damage"

def calculate_basic_attack_damage(attacker, target, base_damage):
    attacker_attack_damage = ((2 * attacker.base_stats["Attack Damage"]) * (attacker.level + 4)) / 100
    
    target_defense = ((2 * target.base_stats["Defence"]) * (target.level + 4)) / 100

    ad_reduction = target_defense / (target_defense + 300)

    ad_multiplier = (((2 * attacker.level) / 5) * base_damage) / 50 
    damage = ad_multiplier + attacker_attack_damage + base_damage/10
    return damage * (1 - ad_reduction)

def calculate_ability_damage(damage_type, attacker, target, base_damage):
    
    # Calculate stats
    attacker_ability_power = ((2 * attacker.base_stats["Ability Power"]) * (attacker.level + 4)) / 100
    attacker_attack_damage = ((2 * attacker.base_stats["Attack Damage"]) * (attacker.level + 4)) / 100
    
    target_magic_resist = ((2 * target.base_stats["Magic Resist"]) * (target.level + 4)) / 100
    target_defense = ((2 * target.base_stats["Defence"]) * (target.level + 4)) / 100

    # Calculate reductions
    ap_reduction = target_magic_resist / (target_magic_resist + 300)
    ad_reduction = target_defense / (target_defense + 300)
    
    # Calculate damage
    if damage_type == DamageType.AD:
        ad_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
        damage = ad_multiplier + attacker_attack_damage + base_damage
        return damage * (1 - ad_reduction)
    
    elif damage_type == DamageType.AP:
        ap_multiplier = (((2 * attacker.level) / 5) * base_damage * 10) / 50
        damage = ap_multiplier + attacker_ability_power + base_damage
        return damage * (1 - ap_reduction)
    
    elif damage_type == DamageType.TRUE_DAMAGE:
        # For true damage, we can directly return the value without any reduction.
        # However, you'll need to specify how much "true damage" an ability does.
        # For this example, I'll assume the true damage is equal to the attacker's level.
        return base_damage
    
    else:
        raise ValueError("Invalid damage type provided.")
