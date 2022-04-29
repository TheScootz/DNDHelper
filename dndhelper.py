import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import DiceRoller
import AudioPlayer


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

        self.audioPlayer = AudioPlayer.AudioPlayer()

        self.playlistWidgetContainer = ttk.Frame(self, width=400, height=800)
        self.playlistWidgetContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

        self.playlistControlsContainer = ttk.Frame(self.playlistWidgetContainer, width=410, height=100, style="BW.TFrame")
        self.playlistControlsContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

        self.playButton = ttk.Button(self.playlistControlsContainer, text="Play",
            command=lambda:self.audioPlayer.play(treeWidget=self.tree, selectedItemID=currentSelection()))

        self.nextButton = ttk.Button(self.playlistControlsContainer, text=">",
            command=lambda:self.audioPlayer.play(treeWidget=self.tree, selectedItemID=self.tree.next(currentSelection())))
        self.prevButton = ttk.Button(self.playlistControlsContainer, text="<",
            command=lambda:self.audioPlayer.play(treeWidget=self.tree, selectedItemID=self.tree.prev(currentSelection())))
        self.playButton.grid(column=1, row=1)        
        self.nextButton.grid(column=2, row=1)
        self.prevButton.grid(column=0, row=1)


        self.tree = ttk.Treeview(self.playlistWidgetContainer, columns=("song_name", "artist_name"), show="headings", height=22)
        self.tree.grid(column=0, row=3, padx=10, pady=10)   

        self.tree.column("song_name")
        self.tree.column("artist_name",width=100)
        self.tree.heading("song_name",text="Name")
        self.tree.heading("artist_name", text="Artist")
        self.tree.tag_configure("simple", background="#E8E8E8")

        self.playlistButtonContainer = ttk.Frame(self.playlistWidgetContainer, width=400, height=120, style="BW.TFrame")
        self.playlistButtonContainer.grid(column=0, row=6, padx=10, pady=10)
        #tag used to differentiate playlist and songs
        playlistTag = "pTag"
        self.tree.tag_configure(playlistTag, background="#E8E8E8")

        self.createPlaylistButton = ttk.Button(self.playlistButtonContainer, text="Create Playlist", 
            command=lambda:self.audioPlayer.createPlaylist(treeWidget=self.tree, tag=playlistTag))

        self.addSongButton = ttk.Button(self.playlistButtonContainer, text="Add Song",
            command=lambda:self.audioPlayer.addSong(treeWidget=self.tree, selectedItemID=currentSelection()))
        #TODO an indexerror will happen if no playlist exists or is selected

        self.deleteButton = ttk.Button(self.playlistButtonContainer, text="Delete",
            command=lambda:self.audioPlayer.deleteItem(treeWidget=self.tree, selectedItemID=currentSelection()))
        self.createPlaylistButton.grid(column=0, row=0, sticky='w')
        self.addSongButton.grid(column=1, row=0)
        self.deleteButton.grid(column=2, row=0, sticky='e')   
        #self.after(0, self.audioPlayer.update())     

        def currentSelection():
            selection=""
            try:
                selection= self.tree.selection()[0]
            except IndexError as e:
                selection=""
                print("nothing selected")
            return selection

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

   
    
if __name__ == "__main__":
    app = DNDHelper()
    app.master.title("D&D Helper")

    app.mainloop()