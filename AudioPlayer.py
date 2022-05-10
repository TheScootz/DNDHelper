import os
from tkinter import ttk, filedialog, simpledialog
from Songs import Song
import pygame
from mutagen.mp3 import MP3
import datetime
import csv

class AudioPlayer:
	def __init__(self):
		self.isPaused=True
		self.fileTypes=(("audio files","*.mp3 *.wav"),("all files","*.*"))
		self.playlistFileTypes=(("csv files","*.csv"),("all files","*.*"))
		pygame.init()
		pygame.mixer.init()
		self.playlistCount=0
		self.playlistSongs=None

	def setUp(self, treeWidget):
		self.tmpWidget=treeWidget


	def play(self, playButton):
		self.playSelected(self.tmpWidget.selection()[0])
		self.isPaused = not self.isPaused
		if (self.isPaused):
			pygame.mixer.music.pause()
			playButton.config(text="Play")
		else:
			pygame.mixer.music.unpause()
			playButton.config(text="||")

	def playSelected(self, selectedItemIID):
		if (selectedItemIID != ""):
			if (selectedItemIID.isdigit()):
				# selected playlist
				children = self.tmpWidget.get_children(selectedItemIID)
				if (len(children) > 0):
					self.playlistSongs = []
					for child in children:
						self.playlistSongs.append(self.tmpWidget.item(child)["values"][2])
					self.playPlaylist()
			else:
				# selected single song that will loop
				self.playSong(path=self.tmpWidget.item(selectedItemIID)["values"][2], loops=-1)


	def playSong(self, path, loops=0):
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(loops=loops)


	def playNextSong(self):
		try:
			nextSelection=self.tmpWidget.next(self.tmpWidget.selection()[0])
			path=self.tmpWidget.item(nextSelection)["values"][2]
			self.tmpWidget.selection_set(path)
			self.playSelected(nextSelection)
		except IndexError as e:
			print("nothing selected")

	def playPrevSong(self):
		try:
			prevSelection=self.tmpWidget.prev(self.tmpWidget.selection()[0])
			path=self.tmpWidget.item(prevSelection)["values"][2]
			self.tmpWidget.selection_set(path)
			self.playSelected(prevSelection)
		except IndexError as e:
			print("nothing selected")

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


	def createPlaylist(self, tag, name):
		self.playlistCount+=1
		self.tmpWidget.insert("", "end", values=(name,"", self.playlistCount), open=False, tags=tag, iid=str(self.playlistCount))


	def addSong(self):
		iid=self.tmpWidget.focus()
		if (iid != ""):
			if (iid.isdigit()):
				path = self.openFile()
				length = ""
				try:
					length = str(datetime.timedelta(seconds=MP3(path).info.length)).split(".")[0]
				except Exception as e:
					length ="N/A"

				tempSong = Song(name=os.path.basename(path), length=length, url=path)
				self.tmpWidget.insert(iid, "end", values=(tempSong.name, tempSong.length, tempSong.url), iid=tempSong.url)


	def deleteItem(self):
		selectedItemID=self.tmpWidget.focus()
		if (selectedItemID != ""):
			selectedItemName = self.tmpWidget.item(selectedItemID)["values"][0]
			#if a playlist was selected for deletion make sure to empty list
			if ("playlist" in selectedItemName):
				self.playlistSongs = []
			self.tmpWidget.delete(selectedItemID)
			pygame.mixer.music.stop()


	def openFile(self):
		return filedialog.askopenfilename(initialdir=".\\Audio",title="Audio Player",filetypes=self.fileTypes)


	def importPlaylists(self):
		fileselected=filedialog.askopenfilename(initialdir=".\\", title="Import Playlist", filetypes=self.playlistFileTypes)
		with open(fileselected) as myfile:
			csvread = csv.reader(myfile, delimiter=',')
			tmpParent=""
			for row in csvread:
				if(row[2].isdigit()):
					tmpParent=row[2]
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


class AudioPlayerWidget(ttk.Frame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.audioPlayer = AudioPlayer()

		self.playlistWidgetContainer = ttk.Frame(self, width=400, height=800)
		self.playlistWidgetContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

		self.playlistControlsContainer = ttk.Frame(self.playlistWidgetContainer, width=410, height=100, style="BW.TFrame")
		self.playlistControlsContainer.grid(column=0, row=0, rowspan=3, padx=10, pady=10)

		self.playButton = ttk.Button(self.playlistControlsContainer, text="Play")
		self.playButton.configure(command=lambda:self.audioPlayer.play(self.playButton))

		self.nextButton = ttk.Button(self.playlistControlsContainer, text=">",
			command=lambda:self.audioPlayer.playNextSong())
		self.prevButton = ttk.Button(self.playlistControlsContainer, text="<",
			command=lambda:self.audioPlayer.playPrevSong())
		self.playButton.grid(column=1, row=1)
		self.nextButton.grid(column=2, row=1)
		self.prevButton.grid(column=0, row=1)


		self.tree = ttk.Treeview(self.playlistWidgetContainer, columns=("song_name", "length_name"), show="headings", height=22)
		self.tree.grid(column=0, row=3, padx=10, pady=10)

		self.audioPlayer.setUp(treeWidget=self.tree)
		self.tree.column("song_name")
		self.tree.column("length_name",width=100)
		self.tree.heading("song_name",text="Name")
		self.tree.heading("length_name", text="Length")

		self.playlistButtonContainer = ttk.Frame(self.playlistWidgetContainer)
		self.playlistButtonContainer.grid(column=0, row=6, padx=10, pady=10)
		#tag used to differentiate playlist and songs
		self.playlistTag = "pTag"
		self.tree.tag_configure(self.playlistTag, background="#E8E8E8")

		self.createPlaylistButton = ttk.Button(self.playlistButtonContainer, text="Create Playlist",
			command=lambda:self.openPlaylistCreateWindow())
		self.addSongButton = ttk.Button(self.playlistButtonContainer, text="Add Song",
			command=lambda:self.audioPlayer.addSong())
		self.deleteButton = ttk.Button(self.playlistButtonContainer, text="Delete",
			command=lambda:self.audioPlayer.deleteItem())
		self.importButton = ttk.Button(self.playlistButtonContainer, text="Import",
			command=lambda:self.audioPlayer.importPlaylists())
		self.exportButton = ttk.Button(self.playlistButtonContainer, text="Export",
			command=lambda:self.audioPlayer.exportPlaylists())

		self.createPlaylistButton.grid(column=0, row=0, sticky='w')
		self.addSongButton.grid(column=1, row=0)
		self.deleteButton.grid(column=2, row=0, sticky='e')
		self.importButton.grid(column=0, row=1)
		self.exportButton.grid(column=1, row=1)

	def openPlaylistCreateWindow(self):
		tmpName = simpledialog.askstring(title="Enter Name", prompt="Enter Playlist Name:")
		self.audioPlayer.createPlaylist(self.playlistTag, tmpName)

