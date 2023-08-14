from battle import interactive_battle_simulation
from venari import Aharas, Akulaw, Algala
from config import akulaw_base_stats, aharas_base_stats, algala_base_stats

# Create teams
player_team = [Aharas("Aharas", aharas_base_stats, 4), Akulaw("Akulaw", akulaw_base_stats, 6), Algala("Algala", algala_base_stats, 5)]
ai_team = [Akulaw("Akulaw", akulaw_base_stats, 5), Akulaw("Akulaw", akulaw_base_stats, 7), Akulaw("Akulaw", akulaw_base_stats, 2)]

# Start the battle simulation
if __name__ == "__main__":
    interactive_battle_simulation(player_team, ai_team)
