from message import Message

class Mailbox(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password

		self.messages = [Message("Hello World!")]

	def messageCount(self):
		return len(self.messages)
	def __len__(self):
		return sum([len(message) for message in self.messages])

	def getMessageIds(self):
		return range(1, len(self.messages) + 1)
	def __getitem__(self, message):
		return self.messages[message - 1]