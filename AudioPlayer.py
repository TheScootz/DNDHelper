import os
from tkinter import filedialog
from Songs import Song
import pygame

class AudioPlayer:
	def __init__(self):
		self.isPaused=False
		self.isPlayingPlaylist=False
		self.fileTypes=(("audio files","*.mp3 *.wav"),("all files","*.*"))
		pygame.mixer.init()
		self.END_SONG_EVENT=pygame.USEREVENT+1
		pygame.mixer.music.set_endevent(self.END_SONG_EVENT) 

	def play(self, treeWidget, selectedItemID):
		self.isPaused = not self.isPaused
		if(self.isPaused):
			pygame.mixer.music.pause()
		else:
			pygame.mixer.music.unpause()

		if(selectedItemID != ""):
			selectedItemName = treeWidget.item(selectedItemID)["values"][0]
			if(selectedItemName == "playlist"):
				print("selected playlist")
				children=treeWidget.get_children(selectedItemID)
				if(len(children) > 0):
					songs=[]
					for child in children:
						songs.append(treeWidget.item(child)["values"][2])

					self.playPlaylist(songsPaths=songs)
					self.isPlayingPlaylist=True
			else:
				print("selected single song")
				self.playSong(path=treeWidget.item(selectedItemID)["values"][2], loops=-1)
				self.isPlayingPlaylist=False

	def playSong(self, path, loops=0):
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(loops=loops)


	def playPlaylist(self, songsPaths):
		self.playSong(songsPaths[0])
		pygame.mixer.music.queue(songsPaths[1])
			#treeWidget.after(0, treeWidget.item(playlistChildren[]))


	def update(self):
		print("update")
		# for event in pygame.event.get():
		# 	if(event.type == self.END_SONG_EVENT):
		# 		playlistChildren=(self.currentSongIndex + 1) % len(self.currentPlaylist)
		# 		playSong();
		

	def createPlaylist(self, treeWidget, tag):
		treeWidget.insert("", "end", values=("playlist",""), open=False, tags=tag)

	def addSong(self, treeWidget, selectedItemID):
		path = self.openFile()
		tempSong = Song(name=os.path.basename(path), artist="unknown", url=path)
		treeWidget.insert(selectedItemID, "end", values=(tempSong.name, tempSong.artist, tempSong.url))


	def deleteItem(self, treeWidget, selectedItemID):
		if(selectedItemID != ""):
			pygame.mixer.music.stop()
			treeWidget.delete(selectedItemID)

	def openFile(self):
		return filedialog.askopenfilename(initialdir=".\\Audio",title="Audio Player",filetypes=self.fileTypes)

