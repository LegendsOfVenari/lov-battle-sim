from .effect import Effect

class Stagger(Effect):
    def __init__(self):
        super().__init__(False, None, 0)

    def description(self):
        return f"Staggers the next basic attack."

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)

        """Override the basic attack for the Venari to remove the Stagger effect after the attack."""
        # Store the original basic attack method
        original_basic_attack = venari.basic_attack

        # Define the new basic attack method
        def new_basic_attack(target, messages):
            # Restore the original attack method
            venari.basic_attack = original_basic_attack
            print(f"{venari.name}({venari.level}) has been staggered")

            # Remove the Stagger effect after the attack
            venari.active_effects = [effect for effect in venari.active_effects if not isinstance(effect, Stagger)]
            messages.append(f"{venari.name}({venari.level})'s Stagger effect has been removed after the basic attack.")

        # Override the Venari's basic attack with the new method
        venari.basic_attack = new_basic_attack
