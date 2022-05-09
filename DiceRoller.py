import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
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


class DiceRollerWidget(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.diceRollerContainer = ttk.Frame(self)
        self.diceRollerLog = scrolledtext.ScrolledText(self, state="disabled", width=40, height=10)

        self.diceRollerContainer.grid(column=0, row=0, padx=10, pady=10, sticky=tk.N)
        self.diceRollerLog.grid(column=0, row=1, padx=10, pady=10, sticky=tk.N+tk.S)


        # Set up Dice Roller interface
        self.diceResult = ttk.Label(self.diceRollerContainer)
        self.diceNum = tk.StringVar()
        self.diceSides = tk.StringVar()
        
        self.diceResult.grid(column=0, row=0, columnspan=5, pady=10)

        ttk.Label(self.diceRollerContainer, text="Roll").grid(column=0, row=1)
        ttk.Entry(self.diceRollerContainer, width=2, textvariable=self.diceNum).grid(column=1, row=1)
        ttk.Label(self.diceRollerContainer, text="dice with").grid(column=2, row=1)
        ttk.Entry(self.diceRollerContainer, width=3, textvariable=self.diceSides).grid(column=3, row=1)
        ttk.Label(self.diceRollerContainer, text="sides").grid(column=4, row=1)

        ttk.Button(self.diceRollerContainer, text="Roll", command=self.rollDice).grid(column=0, row=2, columnspan=5, pady=5)

    
    def rollDice(self, *args):
        self.diceRoller = DiceRoller(int(self.diceNum.get()), int(self.diceSides.get()))
        self.diceRoller.roll()
        self.diceResult.config(text=self.diceRoller.resultString())
        #self.diceResults.insert(0, self.diceRoller.result.copy())
        
        self.diceRollerLog["state"] = "normal"
        self.diceRollerLog.insert("1.0", "{}d{}: {}\n\n".format(self.diceRoller.num, self.diceRoller.sides, self.diceRoller.resultString()))
        self.diceRollerLog["state"] = "disabled"