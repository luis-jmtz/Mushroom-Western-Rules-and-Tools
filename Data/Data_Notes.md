## Creature Ability Notes
id: id (int)
name: name (str)
description: desription (str)
type: type of ability (int)
- 0: utility - movement, cc, non-damaging conditions
- 1: offensive - abilites that deal direct damage
- 2: defensive
points: the amount the ability contributes to the difficulty_level (float)
- for the offensive abilities, need to do a mini_dpr calculation
- will probably need to create a function to add up all the values to add them to the 

---
Might need to multiply offesive points by number of attacks

TL/DR: Advantage and disadvantage are usually the same as a modifier of about +/- 4.5 on your roll.


## Genotype Rules
Genotype IDs:

1. Human
2. Molemen
3. Hulks
4. Scuttlers