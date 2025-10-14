import pandas as pd
import math
from equipment import *
from abilities import *


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
        self.base_speed = 6 # base speed for medium creatures = 30 ft
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
        self.speed = self.base_speed
        self.abilties = []



    def calc_prime(self):
        self.prime = max([self.brawn, self.reflex, self.brains, self.mettle])

    def calc_bonuses(self):
        self.calc_prime()

        self.attack_bonus = self.prime + self.combat_prof
        self.save_dc = 10 + self.attack_bonus

        # Luck represents Health: 6 + Character Level + Might + size
        self.luck = 6 + self.level + self.brawn + self.size
        self.speed = self.base_speed + self.size
        



    # ------------------------------- Add AC values ------------------------------- #

    def add_armor(self, id):
        armor = Armor(id)
        self.armor = armor

    def add_shield(self, id):
        shield = Shield(id)
        self.shield = shield

    def calc_ac(self):
         
        self.calc_bonuses() # calculate current bonuses before doing add. calculations
        
        equipment_ac = 0 # AC from shields and armor

        if self.armor != None:
            equipment_ac += self.armor.ac

            max_reflex = self.prime + self.armor.max_reflex_bonus

            if max_reflex < self.reflex:
                self.reflex = max_reflex

        if self.shield != None:
            equipment_ac += self.shield.ac


        # 8 + Combat Proficiency + Agility + Armor Bonus + Shield Bonus        

        self.ac = 8 + self.combat_prof + self.reflex + equipment_ac



    # --------------------------------- Add Offensive Tools ------------------------ #


    def add_weapon(self, type_id, weapon_id):
        weapon = Weapon(type_id, weapon_id)

        if self.size != 0 & type_id == 0:
            weapon.dmg += self.size

        self.weapons.append(weapon)

    def add_explosives(self, id, count):
        explosive = Explosives(id)

        new_entry = (explosive, count) 
        # tuple that contains the item info, and the number of the item

        self.explosives.append(new_entry)


    
    def calc_dpr(self):
        '''Calculate the Damage per Round
        We will assume that the target has an AC of 10 and that the creature always lands hits the target by rolling a 10
        Next we will assume that combat lasts for 5 rounds, so we'll calculate the average damage per round
        with that in mind.
        '''
        self.calc_bonuses() # calculate current bonuses before doing add. calculations

        heavy_hit_bonus = 0 # bonus damage from a heavy or brutal hit

        # checks if the creature can consistenly hit a higher degree of success on an attack
        if self.attack_bonus > 4:
            if 4 < self.attack_bonus < 10:
                heavy_hit_bonus = 1
            
            elif self.attack_bonus >= 10:
                heavy_hit_bonus = 2

        
        # calculates weapon damage per hit
        damage_list = []
        max_weapon_damage = 0
        
        if len(self.weapons) >0:
            for weapon in self.weapons:
                damage_list.append(weapon.dmg)

            max_weapon_damage = max(damage_list) + heavy_hit_bonus



        # calculates damage from explosives
        explosives_damage = 0

        if len(self.explosives) > 0:
            curr_dmg_bonus = 0

            for y in self.explosives:
                curr_dmg_bonus += y[0].dmg *y[0].radius * y[1]

            explosives_damage = curr_dmg_bonus

        
        damage_per_round = ((max_weapon_damage * self.num_attacks) + explosives_damage) / 5

        self.dpr = damage_per_round

    # --------------------------- Add Abilities -------------------------- #

    def add_ability(self, id):
        ability = Ability(id)

        # name = ability.name
        # score = ability.points

        # new_entry = (name,score)

        self.abilties.append(ability)


    # ----------------------- Calculate Difficulty ---------------------- #

    def calculate_difficulty(self):
        """Calculate creature difficulty level based on core combat stats"""
        self.calc_bonuses() # calculate bonuses first
        
        # Calculate total attribute value
        total_attributes = self.brawn + self.reflex + self.brains + self.mettle
        
        # Base difficulty from level
        base_difficulty = self.level
        
        # Offensive difficulty component
        offensive_score = 0
        
        self.calc_dpr()
        
        # Scale DPR contribution
        offensive_score += self.dpr * 0.5
        # print(f"Offenseive Score: {offensive_score}")
        
        # Bonus for focus points (resource management)
        offensive_score += self.focus_points * 0.5
        
        # Defensive difficulty component
        defensive_score = 0
        
        self.calc_ac()

        # AC contribution: Base AC is 8
        defensive_score += (self.ac - 8) * 0.5
        
        # Luck (HP) contribution: base Luck is 6
        defensive_score += (self.luck - 6) * 0.1
        
        # Damage reduction from armor
        if self.armor and hasattr(self.armor, 'damage_reduction'):
            defensive_score += self.armor.damage_reduction * 2

        # print(f"Defensive Score: {defensive_score}")
        
        # Action economy
        action_score = (self.ap - 2) * 1.5  # Base 2 AP as reference

        ability_score = 0
        if len(self.abilties) != 0:
            for ability in self.abilties:
                points = ability.points
                ability_score += points
        
        # Combine all components
        total_difficulty = (
            base_difficulty +
            offensive_score +
            defensive_score +
            ability_score +
            action_score +
            (total_attributes * 0.2)
        )
        
        # Ensure minimum difficulty
        # total_difficulty = max(1, total_difficulty)
        
        return total_difficulty