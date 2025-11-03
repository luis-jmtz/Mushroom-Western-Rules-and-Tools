# class that inherits creatures class to build player characters
from creatures import Creature
import streamlit as st
import pandas as pd

#load skills data
# skills = pd.read_csv(r"Data\Player_Specific_Data\Skills.tsv", sep="\t")

class player_character(Creature):
    
    def __init__(self):
        super().__init__()

        self.pc_class = 0  # player classes id
        self.core_genotype = 0  # player genotypes id
        self.second_genotype = 0
        self.skill_points = 0
        self.skills = pd.read_csv(r"Data\Player_Specific_Data\Skills.tsv", sep="\t")
        self.save_proficiencies = []  # list of attributes with save proficiency
        self.feats = []  # list of feats the character has
        self.additional_attribute_points = 2
        self.life = 0 # life - when you run out of luck

        self.level = 1

        self.calc_bonuses()
        self.init_core_traits()
        self.calc_skill_points()

    
    def calc_skill_points(self):
        self.skill_points += self.brains + 5

    def init_core_traits(self):
        match self.core_genotype:
            case 1:
                self.additional_attribute_points += 1 # attribute increase
                self.life += 1 # Human Resolve
                self.skill_points += 1 # flexibility
                self.speed = 6
                self.size = 0

            case 2:
                self.size = 0
                self.speed = 5
                self.luck += 1 # tough

            case 3:
                self.size = 0
                self.speed = 6
                
            case 4:
                self.size = -1
                self.speed = 5
                

# need to find way to select which secondary traits to add



    def init_class_abilities(self):
        pass




# Test Area

test = player_character()

test.core_genotype = 4
test.init_core_traits()



for attr_name in dir(test):
    if not attr_name.startswith('__'):
        attr_value = getattr(test, attr_name)
        if not callable(attr_value):  # Skip methods/functions
            if attr_name == 'skills':
                st.subheader("Skills")
                st.dataframe(attr_value)
            else:
                st.write(f"**{attr_name}:** {attr_value}")