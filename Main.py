import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
import pprint


test = Creature()
test.reflex = 2
test.calc_bonuses()

print(test.prime)
print(test.luck)

test.size = -1
test.calc_bonuses()


print(test.attack_bonus)
print(test.save_dc)