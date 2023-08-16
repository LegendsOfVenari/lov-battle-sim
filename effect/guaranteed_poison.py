from .effect import Effect
from .poison import Poison


class GuaranteedPoison(Effect):
    def __init__(self):
        super().__init__(False, None, 0)

    def description(self):
        return f"Guaranteed Poison on next basic attack."

    def on_apply(self, venari, messages):
        super().on_apply(venari, messages)
        # When applied, attach a one-time callback to the Venari's next attack
        original_basic_attack = venari.basic_attack

        def new_basic_attack(target, messages):
            venari.basic_attack = original_basic_attack  # Restore the original attack method
            original_basic_attack(target)  # Perform the original attack

            # Apply the poison effect ONLY if not already applied by Aharas' regular attack
            if not getattr(venari, 'poison_applied', False):
                messages.append(f"Guaranteed Poison!")
                target.apply_effect(Poison(), messages)

            # Remove the GuaranteedPoison effect after it's used
            venari.active_effects = [effect for effect in venari.active_effects if not isinstance(effect, GuaranteedPoison)]

        venari.basic_attack = new_basic_attack
