import pandas as pd
import math


# Load data files
armor = pd.read_csv(r"Data\Armor.tsv", sep="\t")
shields = pd.read_csv(r"Data\Shields.tsv", sep="\t")
melee = pd.read_csv(r"Data\Melee.tsv", sep="\t")
projectile = pd.read_csv(r"Data\Projectile.tsv", sep="\t")
firearms = pd.read_csv(r"Data\Firearms.tsv", sep="\t")
explosives = pd.read_csv(r"Data\Explosives.tsv", sep="\t")

weapons_df = [melee, projectile,firearms]


class Armor:
    def __init__(self):
        self.armor_id = 0

class Weapon:
    def __init__(self, type, id):
        self.weapon_type = type
        #melee, projectile, firearms
        self.weapon_id = id
        chosen_type = weapons_df[self.weapon_type]

        weapon_choice = chosen_type[chosen_type["id"] == self.weapon_id].iloc[0]

        self.damage = weapon_choice.get("dmg")










class Shield:
    def __init__(self):
        self.shield_id = 0

class Explosives:
    def __init__(self):
        self.explosive_id = 0