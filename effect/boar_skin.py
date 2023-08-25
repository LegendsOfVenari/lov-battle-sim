from .effect import Effect
from .armor import Armor


class BoarSkin(Effect):
    def __init__(self,
                 messages,
                 expired=False,
                 is_permanent=True,
                 ad_buff=0,
                 total_armor_distributed=0,
                 total_damage_received=0):
        super().__init__(messages, None, expired, is_permanent)
        # Gain 10% AD and 1 Armor for every 30% missing health
        self.effect_id = "boar_skin"
        self.ad_buff = ad_buff
        self.total_armor_distributed = total_armor_distributed
        self.total_damage_received = total_damage_received

    def description(self):
        return f"Boar Skin +{round(self.ad_buff, 2)} AD"

    def on_apply(self, venari):
        super().on_apply(venari)


    def on_remove(self, venari):
        # Passive Effect cannot be removed
        pass

    def on_damage_received(self, venari, damage):
        self.total_damage_received += damage

        hp_percentage = self.total_damage_received / venari.battle_stats.initial_hp
        calculatedStacks = int(hp_percentage * 10 / 3) # This gives the number of 30% chunks

        if self.total_armor_distributed != calculatedStacks:
            self.distributeBonus(venari, calculatedStacks)
            self.total_armor_distributed = calculatedStacks

    def distributeBonus(self, venari, calculatedStacks):
        venari.battle_stats.attack_damage -= self.ad_buff
        self.ad_buff = (0.1 * venari.battle_stats.attack_damage) * calculatedStacks
        venari.battle_stats.attack_damage += self.ad_buff
        difference_in_stacks = calculatedStacks - self.total_armor_distributed
        for _ in range(difference_in_stacks):
            venari.apply_effect(Armor(self.messages))

        self.messages.append(f"{venari.name} gained {self.ad_buff} attack damage and {difference_in_stacks} armor!")

    def serialize(self):
        return {
            'name': self.__class__.__name__,
            'description': self.description(),
            'expired': self.expired,
            'is_permanent': self.is_permanent,
            'ad_buff': self.ad_buff,
            'total_armor_distributed': self.total_armor_distributed,
            'total_damage_received': self.total_damage_received
        }

    @classmethod
    def deserialize(cls, data, messages):
        print(data)
        return BoarSkin(messages,
                             data["expired"],
                             data["is_permanent"],
                             data["ad_buff"],
                             data["total_armor_distributed"],
                             data["total_damage_received"])
