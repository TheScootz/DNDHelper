import os
from tkinter import filedialog
from Songs import Song
import pygame
from mutagen.mp3 import MP3
import datetime
import csv

class AudioPlayer:
	def __init__(self):
		self.isPaused=False
		self.fileTypes=(("audio files","*.mp3 *.wav"),("all files","*.*"))
		self.playlistFileTypes=(("csv files","*.csv"),("all files","*.*"))
		pygame.init()
		pygame.mixer.init()
		self.playlistCount=0
		self.playlistSongs=None

	def setUp(self, treeWidget):
		self.tmpWidget=treeWidget


	def play(self):
		self.isPaused = not self.isPaused
		if(self.isPaused):
			pygame.mixer.music.pause()
		else:
			pygame.mixer.music.unpause()
		self.playSelected(self.currentSelection())


	def playSelected(self, selectedItemID):
		if (selectedItemID != ""):
			selectedItemName = self.tmpWidget.item(selectedItemID)["values"][0]
			if ("playlist" in selectedItemName):
				# selected playlist
				children = self.tmpWidget.get_children(selectedItemID)
				if (len(children) > 0):
					self.playlistSongs = []
					for child in children:
						self.playlistSongs.append(self.tmpWidget.item(child)["values"][2])
					self.playPlaylist()
			else:
				# selected single song that will loop
				self.playSong(path=self.tmpWidget.item(selectedItemID)["values"][2], loops=-1)


	def playSong(self, path, loops=0):
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(loops=loops)


	def playNextSong(self):
		nextSelection=self.tmpWidget.next(self.currentSelection())
		path=self.tmpWidget.item(nextSelection)["values"][2]
		self.tmpWidget.selection_set(path)
		self.playSelected(nextSelection)


	def playPrevSong(self):
		prevSelection=self.tmpWidget.prev(self.currentSelection())
		path=self.tmpWidget.item(prevSelection)["values"][2]
		self.tmpWidget.selection_set(path)
		self.playSelected(prevSelection)


	def playPlaylist(self):
		if(len(self.playlistSongs) > 0):
			path=self.playlistSongs.pop(0)
			self.playSong(path)
			self.tmpWidget.selection_set(path)
			self.updatePlaylist()


	def updatePlaylist(self):
		currentTime=pygame.mixer.music.get_pos()/1000
		if(currentTime < 0):
			self.playPlaylist()
			return
		self.tmpWidget.after(1000, self.updatePlaylist)


	def createPlaylist(self, tag):
		self.playlistCount+=1
		self.tmpWidget.insert("", "end", values=("playlist"+str(self.playlistCount),""), open=False, tags=tag)


	def addSong(self):
		selectedItemID=self.currentSelection()
		if (selectedItemID != ""):
			selectedItemName = self.tmpWidget.item(selectedItemID)["values"][0]
			if ("playlist" in selectedItemName):
				path = self.openFile()
				length = ""
				try:
					length = str(datetime.timedelta(seconds=MP3(path).info.length)).split(".")[0]
				except Exception as e:
					length ="N/A"

				tempSong = Song(name=os.path.basename(path), length=length, url=path)
				self.tmpWidget.insert(selectedItemID, "end", values=(tempSong.name, tempSong.length, tempSong.url), iid=tempSong.url)


	def deleteItem(self):
		selectedItemID=self.currentSelection()
		if (selectedItemID != ""):
			selectedItemName = self.tmpWidget.item(selectedItemID)["values"][0]
			#if a playlist was selected for deletion make sure to empty list
			if ("playlist" in selectedItemName):
				self.playlistSongs = []
			self.tmpWidget.delete(selectedItemID)
			pygame.mixer.music.stop()


	def openFile(self):
		return filedialog.askopenfilename(initialdir=".\\Audio",title="Audio Player",filetypes=self.fileTypes)


	def currentSelection(self):
		selection = ""
		try:
			selection = self.tmpWidget.selection()[0]
		except IndexError as e:
			selection = ""
			print("nothing selected")
		return selection

	def importPlaylists(self):
		fileselected=filedialog.askopenfilename(initialdir=".\\", title="Import Playlist", filetypes=self.playlistFileTypes)
		with open(fileselected) as myfile:
			csvread = csv.reader(myfile, delimiter=',')
			tmpParent=""
			for row in csvread:
				if("playlist" in row[0]):
					tmpParent=row[0]
					self.tmpWidget.insert("", "end", values=row, iid=tmpParent)
				else:
					self.tmpWidget.insert(tmpParent, "end", values=row, iid=row[2])

	def exportPlaylists(self):
		fileToSave = filedialog.asksaveasfilename(initialdir=".\\", title="Export Playlist", filetypes=self.playlistFileTypes)
		with open(fileToSave, "w", newline="") as myfile:
			csvwriter = csv.writer(myfile, delimiter=",")
			for playlist in self.tmpWidget.get_children():
				row = self.tmpWidget.item(playlist)["values"]
				csvwriter.writerow(row)
				for song in self.tmpWidget.get_children(playlist):
					row = self.tmpWidget.item(song)["values"]
					csvwriter.writerow(row)


