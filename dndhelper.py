import tkinter as tk
from tkinter import ttk
import DiceRoller

if __name__ == "__main__":
    root = tk.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    diceRoller = DiceRoller.DiceRoller(2, 6)
    l = ttk.Label(frame)
    ttk.Button(frame, text="Roll 2d6", command=lambda: diceRoller.rollAndDisplay(l)).grid(column=0, row=0)

    root.mainloop()