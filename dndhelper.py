import tkinter as tk
from tkinter import *
from tkinter import ttk

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
        # Create GUI elements and add them to the grid
        self.createPlaylistWidget()
        self.createMapWidget()
        self.createDiceRollerWidget()

    def createPlaylistWidget(self):
        self.audioPlayerFrame = ttk.Frame(self, width=100, height=500)
        self.audioPlayerFrame.grid();

        # progress = ttk.Progressbar(self.audioPlayerFrame, orient="horizontal", length=300, mode="determinate",value=90)
        # progress.grid(column=0, row = 0, columnspan=5)

        self.tree = ttk.Treeview(self.audioPlayerFrame, columns=("song_name", "artist_name"), show="headings", height=10)
        self.tree.grid(column=0, row=2, columnspan=3)   

        self.tree.column("song_name", anchor=CENTER, stretch=NO)
        self.tree.column("artist_name", anchor=CENTER, stretch=YES, width=100)

        self.tree.heading("song_name",text="Name")
        self.tree.heading("artist_name", text="Artist")
        self.tree.tag_configure("simple", background="#E8E8E8")

    def createPlaylistEntry(self, name, artist, id):
        try:
            selectedItem = self.tree.selection()[0]
            self.tree.insert(selectedItem, tk.END, values=(name,artist), iid=id, open=False)
        except:
            self.tree.insert("", tk.END, values=(name,artist), iid=id, open=False)

    def removeSelectedPlaylistEntry(self):
        try:
            selectedItem = self.tree.selection()[0]
            self.tree.delete(selectedItem)
            return selectedItem
        except:
            print("nothing selected")

    def createPlaylist(self, name):
        self.tree.insert("", tk.END, values=(name,""), open=False, tags=("simple"))

    # def updateSongProgress(self, num):
    #     self.update_idletasks()
    #     self.progress['value'] = num

    def createMapWidget(self):
        self.mapContainer = tk.Canvas(self, bg='#000', width=800, height=600)
        self.mapContainer.grid(column=1, row=0, rowspan=2, padx=10, pady=10)

    def createDiceRollerWidget(self):
        self.diceRollerContainer = tk.Canvas(self, width=400, height=200)
        self.diceRollerLogContainer = tk.Canvas(self, bg='#000', width=400, height=400)
        self.diceRollerContainer.grid(column=2, row=0, padx=10, pady=10)
        self.diceRollerLogContainer.grid(column=2, row=1, padx=10, pady=10)
    
if __name__ == "__main__":
    app = DNDHelper()
    app.master.title("D&D Helper")

    diceRoller = DiceRoller.DiceRoller(2, 6)
    rollText = ttk.Label(app.diceRollerContainer)
    ttk.Button(app.diceRollerContainer, text="Roll 2d6", command=lambda: diceRoller.rollAndDisplay(rollText)).grid(column=0, row=1)

    #setting up audio player
    audioPlayer = AudioPlayer.AudioPlayer(10,10)
    playButton = ttk.Button(app.audioPlayerFrame, text="Play")
    playButton.grid(column=1, row=1)

    playButton.configure(command=lambda: audioPlayer.play(playButton))
    ttk.Button(app.audioPlayerFrame, text="<", command=audioPlayer.skipBack).grid(column=0, row=1)
    ttk.Button(app.audioPlayerFrame, text=">", command=audioPlayer.skipForward).grid(column=2, row=1)

    ttk.Button(app.audioPlayerFrame, text="add song", command=lambda: audioPlayer.add(app.createPlaylistEntry)).grid(column=0, row=3)
    ttk.Button(app.audioPlayerFrame, text="remove song", command=lambda: audioPlayer.remove(app.removeSelectedPlaylistEntry)).grid(column=2, row=3)
    ttk.Button(app.audioPlayerFrame, text="create playlist", command=lambda: app.createPlaylist("playlist")).grid(column=0, row=4)

    app.mainloop()