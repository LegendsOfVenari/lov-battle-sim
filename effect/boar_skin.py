from .effect import Effect
from .armor import Armor


class BoarSkin(Effect):
    def __init__(self,
                 messages,
                 expired=False,
                 is_permanent=True,
                 ad_buff=0,
                 stacks=0):
        super().__init__(messages, None, expired, is_permanent)
        # Gain 10% AD and 1 Armor for every 30% missing health
        self.effect_id = "boar_skin"
        self.ad_buff = ad_buff
        self.stacks = stacks

    def description(self):
        return f"Boar Skin +{round(self.ad_buff, 2)} AD"

    def on_apply(self, venari):
        super().on_apply(venari)


    def on_remove(self, venari):
        # Passive Effect cannot be removed
        pass

    def on_damage_received(self, venari, damage):
        calculatedStacks = self.num_stacks(venari)
        difference_in_stacks = calculatedStacks - self.stacks
        if self.stacks != calculatedStacks:
            self.stacks = calculatedStacks
            self.distributeBonus(venari, difference_in_stacks)

    def on_heal_received(self, venari, heal):
        pass

    def distributeBonus(self, venari, difference_in_stacks):
        venari.battle_stats.attack_damage -= self.ad_buff
        self.ad_buff = (0.1 * venari.battle_stats.attack_damage) * self.stacks
        venari.battle_stats.attack_damage += self.ad_buff
        for _ in range(difference_in_stacks):
            venari.apply_effect(Armor(self.messages))

        self.messages.append(f"{venari.name} gained {self.ad_buff} attack damage and {difference_in_stacks} armor!")


    def num_stacks(self, venari):
        current_hp_percentage = (venari.battle_stats.hp / venari.battle_stats.initial_hp) * 100
        if 70 <= current_hp_percentage <= 100:
            return 0
        elif 40 <= current_hp_percentage < 70:
            return 1
        elif 10 <= current_hp_percentage < 40:
            return 2
        else:
            return 3

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'ad_buff': self.ad_buff,
            'stacks': self.stacks
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return BoarSkin(messages,
                             data["expired"],
                             data["is_permanent"],
                             data["ad_buff"],
                             data["stacks"])
