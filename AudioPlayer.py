import os
from tkinter import filedialog
from Songs import Song
import pygame
from mutagen.mp3 import MP3
import datetime

class AudioPlayer:
	def __init__(self):
		self.isPaused=False
		self.fileTypes=(("audio files","*.mp3 *.wav"),("all files","*.*"))
		pygame.init()
		pygame.mixer.init()
		self.playlistCount=0
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
			if("playlist" in selectedItemName):
				# selected playlist
				children=treeWidget.get_children(selectedItemID)
				if(len(children) > 0):
					songs=[]
					for child in children:
						songs.append(treeWidget.item(child)["values"][2])
					self.playPlaylist(songsPaths=songs)
			else:
				#selected single song that will loop
				self.playSong(path=treeWidget.item(selectedItemID)["values"][2], loops=-1)


	def playSong(self, path, loops=0):
		#print(path)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(loops=loops)


	def playPlaylist(self, songsPaths):
		self.playSong(songsPaths[0])
		#pygame.mixer.music.queue(songsPaths[1])


	#def update(self):
		#print("update")
		# for event in pygame.event.get():
		# 	if(event.type == self.END_SONG_EVENT):
		# 		playlistChildren=(self.currentSongIndex + 1) % len(self.currentPlaylist)
		# 		playSong();
		

	def createPlaylist(self, treeWidget, tag):
		self.playlistCount+=1
		treeWidget.insert("", "end", values=("playlist"+str(self.playlistCount),""), open=False, tags=tag)


	def addSong(self, treeWidget, selectedItemID):
		if (selectedItemID != ""):
			selectedItemName = treeWidget.item(selectedItemID)["values"][0]
			if ("playlist" in selectedItemName):
				path = self.openFile()
				length = ""
				try:
					length = datetime.timedelta(seconds=MP3(path).info.length)
				except Exception as e:
					length ="N/A"

				tempSong = Song(name=os.path.basename(path), length=length, url=path)
				treeWidget.insert(selectedItemID, "end", values=(tempSong.name, tempSong.length, tempSong.url))


	def deleteItem(self, treeWidget, selectedItemID):
		if(selectedItemID != ""):
			pygame.mixer.music.stop()
			treeWidget.delete(selectedItemID)


	def openFile(self):
		return filedialog.askopenfilename(initialdir=".\\Audio",title="Audio Player",filetypes=self.fileTypes)

