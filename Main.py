import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
import pprint


test = Creature()
test.reflex = 2
test.calc_prime()

test.calc_ac(1, 0)

print(test.ac)

test.calc_ac(0,0)

print(test.ac)