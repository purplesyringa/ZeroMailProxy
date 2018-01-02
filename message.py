import hashlib

class Message(object):
	def __init__(self, data):
		self.data = data

	def __len__(self):
		return len(self.data)

	def __str__(self):
		return self.data

	def uidl(self):
		md5 = hashlib.md5()
		md5.update(self.data)
		return md5.hexdigest()