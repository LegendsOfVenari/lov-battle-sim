from utils import display_team_status
from venari import Venari


class Battle:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def is_game_over(self):
        """Check if the game is over."""
        return all(venari.hp <= 0 for venari in self.team1) or all(venari.hp <= 0 for venari in self.team2)

    def auto_swap(self, team, enemy_team):
        # Auto-swap point venari with first bench venari if its HP reaches 0.
        if team[0].hp <= 0 and len(team) > 1:
            print(f"{team[0].name} is defeated!")
            del team[0]
            print(f"{team[0].name} is now the point Venari!")
            team[0].on_swap_in(enemy_team)

    def user_swap(self, team, available_venari):
        print("\nChoose a Venari from the bench to swap with the point Venari:")
        for i, venari in enumerate(available_venari, start=1):
            print(f"{i}. {venari.name}({venari.level})")

        choice = input("Enter the number of the Venari to swap in: ").strip()
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(available_venari):
            print("Invalid choice. Please select a valid Venari number.")
            choice = input("Enter the number of the Venari to swap in: ").strip()

        chosen_venari = available_venari[int(choice) - 1]
        team.remove(chosen_venari)
        team.insert(0, chosen_venari)

        # Call the on_swap_in method for the newly swapped in Venari
        chosen_venari.on_swap_in(self.team2)

    def tick(self):
        """Handle each tick of the battle."""
        if self.team1[0].hp > 0:
            self.team1[0].tick()  # Point venari
            for venari in self.team1[1:]:
                venari.tick(is_point=False)  # Bench venari

        can_attack_status, disrupt_effect_name = self.team1[0].can_attack()
        if not self.team1[0].action_performed and self.team1[0].ready_to_attack and can_attack_status:
            self.team1[0].basic_attack(self.team2[0])
        elif not can_attack_status:
            print(f"{self.team1[0].name}({self.team1[0].level}) is disrupted by {disrupt_effect_name} and cannot attack!")

        if self.team2[0].hp > 0:
            self.team2[0].tick()  # Point venari
            for venari in self.team2[1:]:
                venari.tick(is_point=False)  # Bench venari

        can_attack_status, disrupt_effect_name = self.team2[0].can_attack()
        if not self.team2[0].action_performed and self.team2[0].ready_to_attack and can_attack_status:
            self.team2[0].basic_attack(self.team1[0])
        elif not can_attack_status:
            print(f"{self.team2[0].name}({self.team2[0].level}) is disrupted by {disrupt_effect_name} and cannot attack!")

        # Auto swap Venari if needed
        self.auto_swap(self.team1, self.team2)
        self.auto_swap(self.team2, self.team1)


def interactive_battle_simulation(team1, team2):
    battle = Battle(team1, team2)
    tick = 0

    while not battle.is_game_over() and tick < 100:
        tick += 1
        print(f"\n--- Tick {tick} ---")

        # Display team status
        print("\nPlayer Team Status:")
        display_team_status(team1)

        print("\nAI Team Status:")
        display_team_status(team2)

        # User Decision for Ability
        if team1[0].energy >= 100:
            decision_ability = input(f"Do you want {team1[0].name} to use its ability? (yes/no): ").strip().lower()
            while decision_ability not in ["yes", "no"]:
                print("Invalid choice. Please enter 'yes' or 'no'.")
                prompt = (f"Do you want {team1[0].name} "
                          "to use its ability? (yes/no): ")
                decision_ability = input(prompt).strip().lower()
            if decision_ability == "yes":
                team1[0].use_ability(team2[0])

        # User Decision for Swapping
        """Let the user swap the point Venari with one from the bench."""
        available_venari = [
            venari for venari in team1[1:]
            if venari.swap_cooldown == 0
        ]

        if not available_venari:
            print("No Venari available for swapping due to cooldown!")
        else:
            decision_swap = input("\nDo you want to swap your point Venari with one from the bench? (yes/no): ").strip().lower()
            while decision_swap not in ["yes", "no"]:
                print("Invalid choice. Please enter 'yes' or 'no'.")
                decision_swap = input("Do you want to swap your point Venari with one from the bench? (yes/no): ").strip().lower()

            if decision_swap == "yes":
                battle.user_swap(team1, available_venari)

        # AI Decision for Ability
        if team2[0].energy >= 100:
            team2[0].use_ability(team1[0])

        # AI Decision for Swapping (simple logic: swap if HP is less than 30%)
        max_hp = 10 * team2[0].level + team2[0].constitution * 15 + 100
        if team2[0].hp < 0.3 * max_hp and len(team2) > 1:
            battle.auto_swap(team2, team1)

        battle.tick()

    # Display the winner
    if all(venari.hp <= 0 for venari in team1):
        print("\nTeam 2 (AI) Wins!")
    else:
        print("\nTeam 1 (Player) Wins!")
