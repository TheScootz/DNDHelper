import tkinter as tk
from tkinter import ttk
import DiceRoller
import Chara
import InitTracker
import AudioPlayer
import Map

class DNDHelper(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.createWindow()
        self.createWidgets()

    def createWindow(self):
        self.grid(sticky=(tk.N, tk.W, tk.E, tk.S))
        # Make the window resizeable
        root = self.winfo_toplevel()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # Set the resizing weights of the frame's grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

    def createWidgets(self):
        style = ttk.Style()
        style.configure("BW.TFrame", background='#000')
        # Create GUI elements and add them to the grid
        self.mapWidget = Map.MapWidget(self, width=800, height=800)
        self.mapWidget.grid(column=1, row=0, padx=10, pady=10, rowspan=3, columnspan=2)

        self.diceRollerWidget = DiceRoller.DiceRollerWidget(self)
        self.diceRollerWidget.grid(column=3, row=0, padx=10, pady=10, sticky=tk.N)

        self.characterWidget = Chara.CharacterWidget(self)
        self.characterWidget.grid(column=3, row=1, padx=10, pady=10, sticky = tk.W+tk.N+tk.N)

        self.initiativeWidget = InitTracker.ITrackerWidget(self)
        self.initiativeWidget.grid(column=3, row=0, padx=10, pady=10, sticky = tk.W+tk.S)

        self.audioPlayerWidget = AudioPlayer.AudioPlayerWidget(self)
        self.audioPlayerWidget.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

    
if __name__ == "__main__":
    app = DNDHelper()
    app.master.title("D&D Helper")

    app.mainloop()
    
