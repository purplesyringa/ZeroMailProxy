from message import Message

MESSAGE = "From: Me <me@zeromail.bit>\r\nTo: Wow <wow@zeromail.bit>\r\nSubject: Hello\r\nDate: Fri, 21 Nov 1997 09:55:06 -0600\r\nMessage-ID: zeromail0\r\n\r\nHello!\r\n"

class Mailbox(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password

		self.messages = [Message(MESSAGE), Message(MESSAGE), Message(MESSAGE)]

	def messageCount(self):
		return len(self.messages)
	def __len__(self):
		return sum([len(message) for message in self.messages])

	def getMessageIds(self):
		return range(1, len(self.messages) + 1)
	def __getitem__(self, message):
		return self.messages[message - 1]