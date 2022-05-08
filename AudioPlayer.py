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
		self.playlistSongs=None

	def play(self, treeWidget, selectedItemID):
		self.isPaused = not self.isPaused
		if(self.isPaused):
			pygame.mixer.music.pause()
		else:
			pygame.mixer.music.unpause()
		self.tmpWidget=treeWidget 	#TODO Fix this

		if(selectedItemID != ""):
			selectedItemName = treeWidget.item(selectedItemID)["values"][0]
			if("playlist" in selectedItemName):
				# selected playlist
				children=treeWidget.get_children(selectedItemID)
				if(len(children) > 0):
					self.playlistSongs=[]
					for child in children:
						self.playlistSongs.append(treeWidget.item(child)["values"][2])
					self.playPlaylist()
			else:
				#selected single song that will loop
				self.playSong(path=treeWidget.item(selectedItemID)["values"][2], loops=-1)

	def playSong(self, path, loops=0):
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(loops=loops)


	def playPlaylist(self):
		if(len(self.playlistSongs) > 0):
			self.playSong(self.playlistSongs.pop(0))
			self.updatePlaylist()


	def updatePlaylist(self):
		currentTime=pygame.mixer.music.get_pos()/1000
		#print(currentTime)
		if(currentTime < 0):
			self.playPlaylist()
			return
		self.tmpWidget.after(1000, self.updatePlaylist)


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
