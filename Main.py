import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
from abilities import *

import pprint
import streamlit as st

bandit = Creature()

bandit.brawn = 3
bandit.reflex = 1
bandit.brains = -2
bandit.mettle = 0

bandit.add_armor(1)
bandit.add_weapon(2,6)
bandit.add_weapon(0,9)

bandit.calc_dpr()
print(f"DPR: {bandit.dpr}")

diff = bandit.calculate_difficulty()

print(diff)
