import random

class DiceRoller:
    def __init__(self, num, sides):
        self.num = num
        self.sides = sides
        self.result = []
    
    def roll(self):
        self.result = random.choices(range(1, self.sides+1), k=self.num)

    def resultString(self):
        return ", ".join([str(i) for i in self.result]) + " ({})".format(sum(self.result))