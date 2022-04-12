import random

class DiceRoller:
    def __init__(self, num, sides):
        self.num = num
        self.sides = sides
        self.result = []
    
    def roll(self):
        self.result = random.choices(range(1, self.sides+1), k=self.num)

    def displayResult(self, widget):
        widget.config(text="You rolled {}d{} and got {} = {}".format(self.num, self.sides, self.result, sum(self.result)))
        widget.grid(column=0, row=0)

    def rollAndDisplay(self, widget):
        self.roll()
        self.displayResult(widget)