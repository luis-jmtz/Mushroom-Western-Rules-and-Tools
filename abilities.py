import pandas as pd

# load data
abilities = pd.read_csv(r"Data\Creature_abilities.tsv", sep="\t")

class Ability:
    def __init__(self,id):
        self.ability_id = id

        ability_values = abilities[abilities["id"] == self.ability_id].iloc[0] # returns a series with the values

        self.name = ability_values.get("name")
        self.description = ability_values.get("description")
        self.type = ability_values.get("type")
        self.points = ability_values.get("points")
