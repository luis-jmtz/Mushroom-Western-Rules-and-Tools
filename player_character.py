# class that inherits creatures class to build player characters
from creatures import Creature


class player_character(Creature):
    
    def __init__(self):
        super().__init__()

        self.pc_class = 0  # player classes id
        self.core_genotype = 0  # player genotypes id
        self.second_genotype = 0
        self.skill_points = 0
        self.skills = []  # skill proficiency data
        self.save_proficiencies = []  # list of attributes with save proficiency
        self.feats = []  # list of feats the character has
        self.additional_attribute_points = 2
        self.life = 0 # life - when you run out of luck

        self.level = 1

        self.calc_bonuses()

    
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


    def calc_values(self):

