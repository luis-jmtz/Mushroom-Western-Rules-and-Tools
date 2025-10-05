import pandas as pd
import math
from equipment import *

class Creature:

    def __init__(self):
        #core stats
        self.level = 0
        self.combat_prof = 1 + math.floor(self.level/2)

        #Attributes
        self.brawn = 0
        self.reflex = 0
        self.brains = 0
        self.mettle = 0
        self.prime = 0
        self.calc_prime()


        #physical properties
        self.size = 0 # 0 = medium (standard), 1 = large, 2 = huge, -1 = small
        self.base_speed = 0
        self.canFly = False
        self.canBurrow = False
        self.ap = 2 #min 2 AP
        self.num_attacks = 1 # number of normal attacks
        self.focus_points = 0

        # equipment  
        self.armor = None
        self.shield = None
        self.weapons = []
        self.explosives = []
        
        # combat stats
        self.ac = 0
        self.attack_bonus = 0
        self.save_dc = 0
        self.luck = 0
        self.speed = 0



    def calc_prime(self):
        self.prime = max([self.brawn, self.reflex, self.brains, self.mettle])

    def calc_bonuses(self):
        self.calc_prime()

        self.attack_bonus = self.prime + self.combat_prof
        self.save_dc = 10 + self.attack_bonus

        # Luck represents Health: 6 + Character Level + Might + size
        self.luck = 6 + self.level + self.brawn + self.size
        



# ----------------- Add AC values ------------------------------- #

    def add_armor(self, id):
        armor = Armor(id)
        return armor

    def add_shield(self, id):
        shield = Shield(id)
        return shield

    def calc_ac(self, armor_id, shield_id):
        # load equipment
        self.armor = self.add_armor(armor_id)
        self.shield = self.add_shield(shield_id)

        # 8 + Combat Proficiency + Agility + Armor Bonus + Shield Bonus

        # Calculate the max reflex bonus
        
        max_reflex = self.prime + self.armor.max_reflex_bonus

        if max_reflex < self.reflex:
            self.reflex = max_reflex

        self.ac = 8 + self.combat_prof + self.reflex + self.armor.ac + self.shield.ac
        self.calc_prime()



# ------------------ Add Offensive Tools -------------- #


    def add_weapon(self, type_id, weapon_id):
        weapon = Weapon(type_id, weapon_id)
        
        self.weapons.append(weapon)

    def add_explosives(self, id, count):
        explosive = Explosives(id)

        new_entry = (explosive, count) # tuple that contains the item info, and the number of the item

        self.explosives.append(new_entry)

