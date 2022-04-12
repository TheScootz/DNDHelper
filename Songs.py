from abc import abstractmethod

class IComponent():

	@abstractmethod
	def play(self):
		raise NotImplementedError

	@abstractmethod
	def pause(self):
		raise NotImplementedError

	@abstractmethod
	def stop(self):
		raise NotImplementedError

	@abstractmethod
	def print(self):
		raise NotImplementedError


class Song():

	def __init__(self, name, artist, url):
		self.name = name;
		self.url = url;
		self.artist = artist;

	def play(self):
		print("playing")

	def pause(self):
		print("paused")

	def stop(self):
		print("stopped")

	def print(self):
		print(self.name, " by:", self.artist)


class Playlist(IComponent):

	def __init__(self, name):
		self.name = name
		self.components = []

	def add(self, song):
		self.components.append(song)

	def remove(self, song):
		self.components.remove(song);

	def print(self):
		print(self.name)
		for i in range(len(self.components)):
			self.components[i].print();

	def play(self):
		print("playing")

	def pause(self):
		print("paused")

	def stop(self):
		print("stopped")