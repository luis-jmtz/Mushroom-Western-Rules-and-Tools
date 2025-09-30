import pandas as pd
import math

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

        #physical properties
        self.size = 0
        self.base_speed = 0
        self.canFly = False
        self.canBurrow = False
        self.ap = 2 #min 2 AP
        self.num_attacks = 0 # number of normal attacks
        self.focus_points = 0
        self.isMartial = 0 

        #equipment
        self.ac = 0
        self.attack_bonus = 0
        self.save_dc = 0
        self.luck = 0
        self.speed = 0


    def add_armor(self):
        pass

    def add_shield(self):
        pass

    def add_weapon(self):
        pass

    def add_explosives(self):
        pass