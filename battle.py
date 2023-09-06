from venari import Venari
from enum import Enum

class ActionType(Enum):
    SWAP = "swap"
    ABILITY = "ability"
    NEXT_TICK = "next_tick"
    NEW_GAME = "new_game"

class Battle:
    def __init__(self, team1, team2, tick_count, messages, team1_arena_effects=None, team2_arena_effects=None):
        self.team1 = team1
        self.team2 = team2
        self.team1_arena_effects = team1_arena_effects
        self.team2_arena_effects = team2_arena_effects
        self.messages = messages
        self.action_queue = []
        self.tick_count = tick_count

    def is_game_over(self):
        """Check if the game is over."""
        return all(venari.battle_stats.hp <= 0 for venari in self.team1) or all(venari.battle_stats.hp <= 0 for venari in self.team2)

    def get_ally_team(self, venari):
        for v in self.team1:
            if v is venari:
                return self.team1
        for v in self.team2:
            if v is venari:
                return self.team2
        return None

    def get_enemy_team(self, venari):
        if self.get_ally_team(venari) is self.team1:
            return self.team2
        else:
            return self.team1

    def add_ally_arena_effect(self, arena_effect, venari):
        ally_team = self.get_ally_team(venari)
        self.add_arena_effect(arena_effect, ally_team)

    def add_enemy_arena_effect(self, arena_effect, venari):
        enemy_team = self.get_enemy_team(venari)
        self.add_arena_effect(arena_effect, enemy_team)

    def add_arena_effect(self, arena_effect, team):
        if team == self.team1:
            self.team1_arena_effects[arena_effect.arena_effect_id] = arena_effect
        elif team == self.team2:
            self.team2_arena_effects[arena_effect.arena_effect_id] = arena_effect

    def trigger_arena_effect_swap_in(self, venari, arena_effects):
        for arena_effect in list(arena_effects.values()):
            arena_effect.on_swap_in(venari)

    def has_arena_effect(self, arena_effect_id, venari):
        if self.get_ally_team(venari) == self.team1:
            return arena_effect_id in self.team1_arena_effects
        else:
            return arena_effect_id in self.team2_arena_effects

    def remove_ally_arena_effect(self, arena_effect_id, venari):
        ally_team = self.get_ally_team(venari)
        self.remove_arena_effect(arena_effect_id, ally_team)

    def remove_arena_effect(self, arena_effect_id, team):
        if team == self.team1:
            if arena_effect_id in self.team1_arena_effects:
                arena_effect = self.team1_arena_effects[arena_effect_id]
                arena_effect.remove()
        elif team == self.team2:
            if arena_effect_id in self.team2_arena_effects:
                arena_effect = self.team2_arena_effects[arena_effect_id]
                arena_effect.remove()

    def auto_swap(self, team, enemy_team, traps):
        # Auto-swap point venari with first bench venari if its HP reaches 0.
        if team[0].battle_stats.hp <= 0 and len(team) > 1:
            # Notify effects that ally has been defeated
            for venari in team:
                for effect in venari.battle_handler.active_effects.values():
                    effect.on_ally_defeated()
            del team[0]
            self.trigger_arena_effect_swap_in(team[0], traps)
            team[0].on_swap_in(enemy_team)

    def tick(self):
        # Process the action queue
        while self.action_queue:
            action = self.action_queue.pop(0)
            action()

        # Trigger auras
        for arena_effect in list(self.team1_arena_effects.values()):
            if arena_effect.expired:
                arena_effect.on_remove(self)
                self.team1_arena_effects.pop(arena_effect.arena_effect_id)
            else:
                arena_effect.on_tick(self.team1[0])
                if arena_effect.expired:
                    arena_effect.on_remove(self)
                    self.team1_arena_effects.pop(arena_effect.arena_effect_id)

        for arena_effect2 in list(self.team2_arena_effects.values()):
            if arena_effect2.expired:
                arena_effect2.on_remove(self)
                self.team2_arena_effects.pop(arena_effect2.arena_effect_id)
            else:
                arena_effect2.on_tick(self.team2[0])
                if arena_effect2.expired:
                    arena_effect2.on_remove(self)
                    self.team2_arena_effects.pop(arena_effect2.arena_effect_id)

        if self.team1[0].battle_stats.hp > 0:
            self.team1[0].tick()  # Point venari
            for venari in self.team1[1:]:
                venari.tick(is_point=False)  # Bench venari

        if self.team1[0].ready_to_attack():
            self.team1[0].basic_attack(self.team2[0])

        if self.team2[0].battle_stats.hp > 0:
            self.team2[0].tick()  # Point venari
            for venari in self.team2[1:]:
                venari.tick(is_point=False)  # Bench venari

        if self.team2[0].ready_to_attack():
            self.team2[0].basic_attack(self.team1[0])

        # Auto swap Venari if needed
        self.auto_swap(self.team1, self.team2, self.team1_arena_effects)
        self.auto_swap(self.team2, self.team1, self.team2_arena_effects)
        self.tick_count += 1

    def interactive_battle_simulation(self, action, swap_index=None):
        self.messages.append(f"Current Tick: {self.tick_count}")

        if self.is_game_over():
            # If the game is already over, just return the game state and messages
            return {
                "team1_status": self.team1,
                "team2_status": self.team2,
                "messages": ["The game is already over."],
                "tick_count": self.tick_count,
                "team1_arena_effects": self.team1_arena_effects,
                "team2_arena_effects": self.team2_arena_effects
            }

        if action == ActionType.ABILITY:
            if self.team1[0].can_use_ability():
                self.action_queue.append(lambda: self.team1[0].use_ability(self.team2[0]))
            else:
                self.messages.append(f"{self.team1[0].name} does not have enough energy!")

        elif action == ActionType.SWAP and swap_index is not None:
            self._swap_venari(self.team1, swap_index + 1, self.team1_arena_effects)
            self.messages.append(f"Swapped {self.team1[swap_index + 1].name} with {self.team1[0].name}!")
        elif action == ActionType.NEXT_TICK:
            self.messages.append(f"Moved to the next tick without any action.")
        elif action == ActionType.NEW_GAME:
            return {
                "team1_status": self.team1,
                "team2_status": self.team2,
                "messages": ["Starting a new game."],
                "tick_count": 0,
                "team1_arena_effects": self.team1_arena_effects,
                "team2_arena_effects": self.team2_arena_effects
            }

        # AI decisions
        if self.team2[0].can_use_ability():
            self.team2[0].use_ability(self.team1[0])

        elif len(self.team2) > 1 and self.team2[1].can_swap():
            self._swap_venari(self.team2, 1, self.team2_arena_effects)

        elif len(self.team2) > 2 and self.team2[2].can_swap():
            self._swap_venari(self.team2, 2, self.team2_arena_effects)

        # Execute actions in the queue
        self.tick()

        # Determine winner (if game is over)
        if all(venari.battle_stats.hp <= 0 for venari in self.team1):
            self.messages.append("Team 2 (AI) Wins!")
        elif all(venari.battle_stats.hp <= 0 for venari in self.team2):
            self.messages.append("Team 1 (Player) Wins!")

        return {
            "team1_status": self.team1,
            "team2_status": self.team2,
            "messages": self.messages,
            "tick_count": self.tick_count,
            "team1_arena_effects": self.team1_arena_effects,
            "team2_arena_effects": self.team2_arena_effects
        }

    def _swap_venari(self, team, swap_index, traps):
        """Utility function to swap the point Venari with a bench Venari based on the given swap index."""
        # Swap the point Venari with the chosen bench Venari
        team[0], team[swap_index] = team[swap_index], team[0]
        self.trigger_arena_effect_swap_in(team[0], traps)
        team[0].on_swap_in(self.get_enemy_team(team[0]))
