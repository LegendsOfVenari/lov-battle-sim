from utils import display_team_status
from venari import Venari
from enum import Enum

class ActionType(Enum):
    SWAP = "swap"
    ABILITY = "ability"
    NEXT_TICK = "next_tick"
    NEW_GAME = "new_game"

class Battle:
    def __init__(self, team1, team2, tick_count):
        self.team1 = team1
        self.team2 = team2
        self.action_queue = []
        self.tick_count = tick_count

    def is_game_over(self):
        """Check if the game is over."""
        return all(venari.hp <= 0 for venari in self.team1) or all(venari.hp <= 0 for venari in self.team2)

    def auto_swap(self, team, enemy_team, messages):
        # Auto-swap point venari with first bench venari if its HP reaches 0.
        if team[0].hp <= 0 and len(team) > 1:
            print(f"{team[0].name} is defeated!")
            del team[0]
            print(f"{team[0].name} is now the point Venari!")
            team[0].on_swap_in(messages, enemy_team)

    def user_swap(self, team, available_venari, messages):
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
        chosen_venari.on_swap_in(messages, self.team2)

    def tick(self, messages):
        # Process the action queue
        while self.action_queue:
            action = self.action_queue.pop(0)
            action()

        if self.team1[0].hp > 0:
            self.team1[0].tick(messages)  # Point venari
            for venari in self.team1[1:]:
                venari.tick(messages, is_point=False)  # Bench venari

        if not self.team1[0].action_performed and self.team1[0].ready_to_attack:
            self.team1[0].basic_attack(self.team2[0], messages)

        if self.team2[0].hp > 0:
            self.team2[0].tick(messages)  # Point venari
            for venari in self.team2[1:]:
                venari.tick(messages, is_point=False)  # Bench venari

        if not self.team2[0].action_performed and self.team2[0].ready_to_attack:
            self.team2[0].basic_attack(self.team1[0], messages)

        # Auto swap Venari if needed
        self.auto_swap(self.team1, self.team2, messages)
        self.auto_swap(self.team2, self.team1, messages)
        self.tick_count += 1

    def interactive_battle_simulation(self, action, swap_index=None):
        game_messages = []
        game_messages.append(f"Current Tick: {self.tick_count}")

        if self.is_game_over():
            # If the game is already over, just return the game state and messages
            return {
                "team1_status": self.team1,
                "team2_status": self.team2,
                "messages": ["The game is already over."],
                "tick_count": self.tick_count,
            }

        if action == ActionType.ABILITY:
            if self.team1[0].energy >= 100:
                self.action_queue.append(lambda: self.team1[0].use_ability(self.team2[0], game_messages))
            else:
                game_messages.append(f"{self.team1[0].name} does not have enough energy!")

        elif action == ActionType.SWAP and swap_index is not None:
            venari_to_swap = self.team1[swap_index + 1]
            if venari_to_swap and venari_to_swap.swap_cooldown == 0:
                # Swap the point Venari with the chosen bench Venari
                self.team1[0], self.team1[swap_index + 1] = self.team1[swap_index + 1], self.team1[0]
                self.team1[0].on_swap_in(game_messages, self.team2)
                game_messages.append(f"Swapped {self.team1[swap_index + 1].name} with {self.team1[0].name}!")
            else:
                game_messages.append(f"Cannot swap this Venari due to cooldown or other issues.")

        elif action == ActionType.NEXT_TICK:
            game_messages.append(f"Moved to the next tick without any action.")
        elif action == ActionType.NEW_GAME:
            return {
                "team1_status": self.team1,
                "team2_status": self.team2,
                "messages": ["Starting a new game."],
                "tick_count": 0,
            }

        # AI decisions (remain unchanged)
        if self.team2[0].energy >= 100:
            self.team2[0].use_ability(self.team1[0], game_messages)

        max_hp = 10 * self.team2[0].level + self.team2[0].constitution * 15 + 100
        if self.team2[0].hp < 0.3 * max_hp and len(self.team2) > 1:
            self.auto_swap(self.team2, self.team1, game_messages)

        # Execute actions in the queue
        self.tick(game_messages)

        # Determine winner (if game is over)
        if all(venari.hp <= 0 for venari in self.team1):
            game_messages.append("Team 2 (AI) Wins!")
        elif all(venari.hp <= 0 for venari in self.team2):
            game_messages.append("Team 1 (Player) Wins!")

        return {
            "team1_status": self.team1,
            "team2_status": self.team2,
            "messages": game_messages,
            "tick_count": self.tick_count,
        }