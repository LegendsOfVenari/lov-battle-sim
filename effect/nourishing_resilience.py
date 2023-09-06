from .stackable_effect import Effect
import random


class NourishingResilience(Effect):
    def __init__(self,
                 messages):
        super().__init__(messages, None, False, True)
        self.effect_id = "nourishing_reslience"

    def description(self):
        return "Nourishing Resilience"

    def on_damage_received(self, venari, damage):
        # Heal a random wounded ally on the allied bench for 20 AP
        ally_team = venari.get_ally_team()

        # Filter out the wounded allies (we'll assume wounded means HP is less than max HP)
        wounded_allies = [ally for ally in ally_team if ally.battle_stats.hp < ally.battle_stats.initial_hp and ally != venari]

        if wounded_allies:
            # Choose a random wounded ally
            chosen_ally = random.choice(wounded_allies)
            heal_amount = damage * 0.3

            # Apply the heal
            chosen_ally.heal(heal_amount)

            # Add a message or log for this action
            self.messages.append(f"{chosen_ally.name} was healed for {heal_amount} AP due to {venari.name}'s ability!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description()
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return NourishingResilience(messages)
