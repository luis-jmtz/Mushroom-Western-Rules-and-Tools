import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
from abilities import *

import pprint
import streamlit as st

#  load data to get accurate names lists 
abilities = pd.read_csv(r"Data\Creature_abilities.tsv", sep="\t")
armor = pd.read_csv(r"Data\Armor.tsv", sep="\t")
shields = pd.read_csv(r"Data\Shields.tsv", sep="\t")
melee = pd.read_csv(r"Data\Melee.tsv", sep="\t")
projectile = pd.read_csv(r"Data\Projectile.tsv", sep="\t")
firearms = pd.read_csv(r"Data\Firearms.tsv", sep="\t")
explosives = pd.read_csv(r"Data\Explosives.tsv", sep="\t")
weapons_df = [melee, projectile,firearms]



# bandit = Creature()
# bandit.brawn = 3
# bandit.reflex = 1
# bandit.brains = -2
# bandit.mettle = 0

# bandit.add_armor(1)
# bandit.add_weapon(2,6)
# bandit.add_weapon(0,9)

# bandit.calc_dpr()
# print(f"DPR: {bandit.dpr}")

# bandit.add_ability(1)

# diff = bandit.calculate_difficulty()

# print(diff)

# print(bandit.abilties[0].name)

# bandit.add_ability(1)

# diff = bandit.calculate_difficulty()

# print(diff)