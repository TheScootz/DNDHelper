import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import DiceRoller
from Songs import Song, Playlist

class DNDHelper(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.createWindow()
        self.createWidgets()

    def createWindow(self):
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
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
        self.createPlaylistWidget()
        self.createMapWidget()
        self.createDiceRollerWidget()

    def createPlaylistWidget(self):
        self.playlistWidgetContainer = ttk.Frame(self, width=400, height=800)
        self.playlistWidgetContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)
        #self.playlistWidgetContainer.rowconfigure(0, weight=5)
        #self.playlistWidgetContainer.rowconfigure(1, weight=1)

        self.playlistContainer = ttk.Frame(self.playlistWidgetContainer, width=400, height=600, style="BW.TFrame")
        self.playlistContainer.grid(column=0, row=0, padx=10, pady=10)

        self.playlistButtonContainer = ttk.Frame(self.playlistWidgetContainer, width=400, height=120, style="BW.TFrame")
        self.playlistButtonContainer.grid(column=0, row=1, padx=10, pady=10)
        #self.playlistButtonContainer.columnconfigure(0, weight=1)
        #self.playlistButtonContainer.columnconfigure(1, weight=1)
        #self.playlistWidgetContainer.rowconfigure(0, weight=1)

        self.addSongButton = ttk.Button(self.playlistButtonContainer, text="Add Song")
        self.swapPlaylistButton = ttk.Button(self.playlistButtonContainer, text="Swap Playlist")
        self.addSongButton.grid(column=0, row=0, sticky='w')
        self.swapPlaylistButton.grid(column=1, row=0, sticky='e')

    def createMapWidget(self):
        self.mapWidgetContainer = ttk.Frame(self, width=800, height=800)
        self.mapWidgetContainer.grid(column=1, row=0, padx=10, pady=10)

        self.mapContainer = ttk.Frame(self.mapWidgetContainer, width=800, height=600, style="BW.TFrame")
        self.mapContainer.grid(column=0, row=0, padx=10, pady=10)

        self.mapButtonContainer = ttk.Frame(self.mapWidgetContainer, width=800, height=120, style="BW.TFrame")
        self.mapButtonContainer.grid(column=0, row=1, padx=10, pady=10)

        self.setBackgroundButton = ttk.Button(self.mapButtonContainer, text="Set Background")
        self.addCharacterButton = ttk.Button(self.mapButtonContainer, text="Add Character")
        self.addAOEButton = ttk.Button(self.mapButtonContainer, text="Add Area of Effect")
        self.setBackgroundButton.grid(column=0, row=0, sticky='w')
        self.addCharacterButton.grid(column=1, row=0)
        self.addAOEButton.grid(column=2, row=0, sticky='e')

    def createDiceRollerWidget(self):
        # Create containers
        self.diceRollerWidgetContainer = ttk.Frame(self)
        self.diceRollerWidgetContainer.grid(column=2, row=0, padx=10, pady=10, sticky=tk.N)

        self.diceRollerContainer = ttk.Frame(self.diceRollerWidgetContainer)
        self.diceRollerLog = scrolledtext.ScrolledText(self.diceRollerWidgetContainer, state="disabled", width=40)

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


        # Set up Dice Roller log
        #self.diceResults = []

    
    def rollDice(self, *args):
        self.diceRoller = DiceRoller.DiceRoller(int(self.diceNum.get()), int(self.diceSides.get()))
        self.diceRoller.roll()
        self.diceResult.config(text=self.diceRoller.resultString())
        #self.diceResults.insert(0, self.diceRoller.result.copy())
        
        self.diceRollerLog["state"] = "normal"
        self.diceRollerLog.insert("1.0", "{}d{}: {}\n\n".format(self.diceRoller.num, self.diceRoller.sides, self.diceRoller.resultString()))
        self.diceRollerLog["state"] = "disabled"

        


def SongsTest():
    s = Song("song1", "artist1", "url1",)
    s1 = Song("song2", "artist1", "url2")
    s2 = Song("song3", "artist1", "url3")
    s3 = Song("ambience_song4", "artist1", "url4")
    s4 = Song("epic_song", "artist1", "url5")

    m = Playlist("music")
    m.add(s)
    m.add(s1)
    m.add(s2)

    a = Playlist("ambience")
    a.add(s3)

    mainPlaylist = Playlist("dndGame")
    mainPlaylist.add(m)
    mainPlaylist.add(a)
    mainPlaylist.add(s4)
    mainPlaylist.print()

    
if __name__ == "__main__":
    app = DNDHelper()
    app.master.title("D&D Helper")

    app.mainloop()

    SongsTest()