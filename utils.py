def display_team_status(team):
    """Display the status of the given team."""
    next_attack_tick_point = team[0].base_stats["Basic Attack Frequency"] - (team[0].attack_tick_counter % team[0].base_stats["Basic Attack Frequency"])
    print(f"{team[0].name}({team[0].level}) (Point) - HP: {team[0].hp:.2f}, Energy: {team[0].energy}, Next Attack: {next_attack_tick_point} ticks")
    if team[0].active_effects:
        effects = ", ".join(effect.description() for effect in team[0].active_effects)
        print(f"    Active Effects: {effects}")
    
    for venari in team[1:]:
        next_attack_tick_bench = venari.base_stats["Basic Attack Frequency"] - (venari.attack_tick_counter % venari.base_stats["Basic Attack Frequency"])
        swap_cooldown_info = f", Swap Cooldown: {venari.swap_cooldown} ticks" if venari.swap_cooldown > 0 else ""
        print(f"{venari.name}({venari.level}) (Bench) - HP: {venari.hp:.2f}, Energy: {venari.energy}, Next Attack: {next_attack_tick_bench} ticks{swap_cooldown_info}")
        if venari.active_effects:
            effects = ", ".join(effect.description() for effect in venari.active_effects)
            print(f"    Active Effects: {effects}")
