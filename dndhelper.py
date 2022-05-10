import tkinter as tk
from tkinter import ttk
import DiceRoller
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
        self.createPlaylistWidget()
        self.mapWidget = Map.MapWidget(self, width=800, height=800)
        self.mapWidget.grid(column=1, row=0, padx=10, pady=10, rowspan=3, columnspan=2)

        self.diceRollerWidget = DiceRoller.DiceRollerWidget(self)
        self.diceRollerWidget.grid(column=3, row=0, padx=10, pady=10, sticky=tk.N)

        self.createCharacterWidget()
        self.createInitiativeTrackerWidget()

    def createPlaylistWidget(self):

        self.audioPlayer = AudioPlayer.AudioPlayer()

        self.playlistWidgetContainer = ttk.Frame(self, width=400, height=800)
        self.playlistWidgetContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

        self.playlistControlsContainer = ttk.Frame(self.playlistWidgetContainer, width=410, height=100, style="BW.TFrame")
        self.playlistControlsContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

        self.playButton = ttk.Button(self.playlistControlsContainer, text="Play",
            command=lambda:self.audioPlayer.play(treeWidget=self.tree, selectedItemID=currentSelection()))

        self.nextButton = ttk.Button(self.playlistControlsContainer, text=">",
            command=lambda:self.audioPlayer.playNextSong(treeWidget=self.tree, nextSelection=self.tree.next(currentSelection())))
        self.prevButton = ttk.Button(self.playlistControlsContainer, text="<",
            command=lambda:self.audioPlayer.playPrevSong(treeWidget=self.tree, prevSelection=self.tree.prev(currentSelection())))
        self.playButton.grid(column=1, row=1)        
        self.nextButton.grid(column=2, row=1)
        self.prevButton.grid(column=0, row=1)


        self.tree = ttk.Treeview(self.playlistWidgetContainer, columns=("song_name", "length_name"), show="headings", height=22)
        self.tree.grid(column=0, row=3, padx=10, pady=10)   

        self.tree.column("song_name")
        self.tree.column("length_name",width=100)
        self.tree.heading("song_name",text="Name")
        self.tree.heading("length_name", text="Length")

        self.playlistButtonContainer = ttk.Frame(self.playlistWidgetContainer, width=400, height=120, style="BW.TFrame")
        self.playlistButtonContainer.grid(column=0, row=6, padx=10, pady=10)
        #tag used to differentiate playlist and songs
        playlistTag = "pTag"
        self.tree.tag_configure(playlistTag, background="#E8E8E8")

        self.createPlaylistButton = ttk.Button(self.playlistButtonContainer, text="Create Playlist", 
            command=lambda:self.audioPlayer.createPlaylist(treeWidget=self.tree, tag=playlistTag))

        self.addSongButton = ttk.Button(self.playlistButtonContainer, text="Add Song",
            command=lambda:self.audioPlayer.addSong(treeWidget=self.tree, selectedItemID=currentSelection()))

        self.deleteButton = ttk.Button(self.playlistButtonContainer, text="Delete",
            command=lambda:self.audioPlayer.deleteItem(treeWidget=self.tree, selectedItemID=currentSelection()))
        self.createPlaylistButton.grid(column=0, row=0, sticky='w')
        self.addSongButton.grid(column=1, row=0)
        self.deleteButton.grid(column=2, row=0, sticky='e')   

        def currentSelection():
            selection=""
            try:
                selection= self.tree.selection()[0]
            except IndexError as e:
                selection=""
                print("nothing selected")
            return selection
        
    def createCharacterWidget(self):
        self.characterWidgetContainer = ttk.Frame(self, width=350, height=200, style="BW.TFrame")
        self.characterWidgetContainer.grid(column=3, row=1, padx=10, pady=10)


    def createInitiativeTrackerWidget(self):
        self.initiativeTracker = ttk.Frame(self, width=350, height=200, style="BW.TFrame")
        self.initiativeTracker.grid(column=3, row=2, padx=10, pady=10)


   
    
if __name__ == "__main__":
    app = DNDHelper()
    app.master.title("D&D Helper")

    app.mainloop()