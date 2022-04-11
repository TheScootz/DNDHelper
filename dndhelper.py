import tkinter as tk
from tkinter import ttk
import DiceRoller
from Songs import Song, Playlist


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
    root = tk.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    diceRoller = DiceRoller.DiceRoller(2, 6)
    rollText = ttk.Label(frame)
    ttk.Button(frame, text="Roll 2d6", command=lambda: diceRoller.rollAndDisplay(rollText)).grid(column=0, row=0)

    root.mainloop()

    SongsTest()
