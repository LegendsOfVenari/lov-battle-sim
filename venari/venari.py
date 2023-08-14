class Venari:
    def __init__(self, name, base_stats, level):
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.level_up()
        self.energy = 0
        self.attack_tick_counter = 0
        self.active_effects = []  # List to hold active effects
        self.action_performed = False  # New attribute
        self.ready_to_attack = False  # New attribute to track if Venari is ready to attack

    def level_up(self):
        """Calculates stats based on level and base stats."""
        self.constitution = ((2 * self.base_stats["Constitution"] * (self.level + 4)) / 100)
        self.attack_damage = ((2 * self.base_stats["Attack Damage"] * (self.level + 4)) / 100)
        self.ability_power = ((2 * self.base_stats["Ability Power"] * (self.level + 4)) / 100)
        self.defense = ((2 * self.base_stats["Defence"] * (self.level + 4)) / 100)
        self.magic_resist = ((2 * self.base_stats["Magic Resist"] * (self.level + 4)) / 100)
        self.hp = 10 * self.level + self.constitution * 15 + 100

    def apply_effect(self, effect):
        """Apply a new effect to the Venari."""
        self.active_effects.append(effect)
        effect.on_apply(self)

    def tick_effects(self):
        """Process all active effects for the Venari."""
        for effect in self.active_effects:
            effect.on_tick(self)
            effect.tick()
        
        # Remove expired effects
        self.active_effects = [effect for effect in self.active_effects if not effect.expired]

    def basic_attack_damage(self):
        return ((((2 * self.level) / 5) * self.base_stats["Basic Attack Movestat"]) / 50) + self.attack_damage + (self.base_stats["Basic Attack Movestat"] / 10)

    def basic_attack(self, target):
        self.action_performed = True
        self.ready_to_attack = False  # Reset the readiness flag after performing the attack
        self.attack_tick_counter = 0  # Reset the attack tick counter

    def use_ability(self, target):
        self.action_performed = True
    
    def on_swap_in(self, enemy_team=None):
        self.action_performed = True
        self.attack_tick_counter = 0

    def tick(self, is_point=True):
        """What the Venari does every tick."""
        self.reset_action()
        self.energy += self.base_stats["Energy Gain Passively"]
        self.energy = min(self.energy, 100)
        self.tick_effects()

        if is_point:
            # Update attack readiness only for the point Venari
            self.attack_tick_counter += 1
            if self.attack_tick_counter >= self.base_stats["Basic Attack Frequency"]:
                self.ready_to_attack = True
                print(f"{self.name}({self.level}) will attack on the next tick!")
            
    def reset_action(self):
        self.action_performed = False
