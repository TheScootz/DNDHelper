
class Song():

	def __init__(self, name, artist, url, length):
		self.name = name
		self.url = url
		self.artist = artist
		self.length = length


class Playlist():

	def __init__(self, name):
		self.name = name
		self.components = []
		self.i = -1

	def add(self, song):
		self.components.append(song)
		index =  len(self.components) - 1
		print("added: ",index)
		return index

	def remove(self, indexID):
		del self.components[indexID];

	def print(self):
		print(self.name)
		for i in range(len(self.components)):
			self.components[i].print();

	def nextSong(self):
		if(len(self.components) > 0):
			self.i += 1
			currentSong = self.components[self.i % len(self.components)];
			return currentSong.url

	def prevSong(self):
		if(len(self.components) > 0):
			self.i -= 1
			currentSong = self.components[self.i % len(self.components)];
			return currentSong.url