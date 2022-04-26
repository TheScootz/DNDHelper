import os
from tkinter import filedialog
from Songs import Song, Playlist
import pygame
#import vlc

class AudioPlayer:
	def __init__(self, volumeMusic, volumeAmbience):
		self.volumeMusic: volumeMusic
		self.volumeAmbience: volumeAmbience
		self.isPaused = False
		self.mainPlaylist = Playlist("main")
		self.fileTypes = (("audio files","*.mp3 *.wav"),("all files","*.*"))
		pygame.mixer.init()
		#pygame.mixer.music.set_endevent(pygame.USEREVENT)

	def play(self, widget):
		self.isPaused = not self.isPaused
		widget.config(text="Play" if self.isPaused else "||")

		if(not pygame.mixer.music.get_busy()):
			self.loadSong(self.mainPlaylist.nextSong())

		if(self.isPaused):
			pygame.mixer.music.pause()
		else:
			pygame.mixer.music.unpause()

	def skipBack(self):
		self.loadSong(self.mainPlaylist.prevSong())

	def skipForward(self):
		self.loadSong(self.mainPlaylist.nextSong())

	def add(self, func):
		try:
			path = self.openFile()
			tempSong = Song(name=os.path.basename(path), artist="unknown", url=path, length=pygame.mixer.Sound(path).get_length())
			func(name=tempSong.name, artist=tempSong.artist, id=self.mainPlaylist.add(tempSong))
		except:
			print("error: selecting song")

	def remove(self, func):
		pygame.mixer.music.stop()
		id = func()
		self.mainPlaylist.remove(int(id))

	# def update(self):
	# 	for event in pygame.event.get():
	# 		if(event.type in pygame.USEREVENT):
	# 			self.skipForward()


	def openFile(self):
		#should use some error checking
		return filedialog.askopenfilename(initialdir=".\\Audio",title="Audio Player",filetypes=self.fileTypes)
				
	def loadSong(self, url):
		try:
			pygame.mixer.music.load(url)
			pygame.mixer.music.play(loops=0)
		except:
			print("error: no available songs")