import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
import pprint


test = Creature()
test.reflex = 2
test.calc_bonuses()


test.add_explosives(1, 1)

print(test.explosives)

test.add_explosives(2, 2)

print(test.explosives)


print(test.explosives[0][0].dmg)


# test.add_weapon(2,3)

# print(test.weapons)
# print(test.weapons[0].name)

# test.add_weapon(0,5)

# print(test.weapons)
# print(test.weapons[1].name)


# test.add_weapon(1,5)

# print(test.weapons)
# print(test.weapons[2].name)

# print(test.prime)
# print(test.luck)

# test.size = -1
# test.calc_bonuses()


# print(test.attack_bonus)
# print(test.save_dc)