# class that inherits creatures class to build player characters
from creatures import Creature

class player_character(Creature):
    
    def __init__(self):
        super().__init__()

        self.pc_class = 0 # player classes id
        self.genotype = 0   # player genotypes id