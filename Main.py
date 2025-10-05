import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
import pprint

temp = Creature()

temp.size = -1

temp.calc_bonuses()

temp.add_weapon(0,0)

print(temp.weapons[0].name)
print(temp.weapons[0].dmg)
temp.size = -1
temp.calc_bonuses()
print(temp.speed)

