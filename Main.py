import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
import pprint


test = Creature()
test.reflex = 2
test.calc_bonuses()

test.add_weapon(2,3)
test.add_weapon(0,5)
test.add_weapon(1,5)


test.add_explosives(5,1)
test.add_explosives(7, 2)

test.calc_dpr()


# temp =  test.weapons

# for x in temp:
#     print(x.dmg)


# test.calc_dpr()

# print(f"Attack Bonus: {test.attack_bonus}")

# test.attack_bonus = 5

# print(f"New Attack Bonus: {test.attack_bonus}")

# test.calc_dpr()
