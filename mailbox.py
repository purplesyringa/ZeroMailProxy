import zeromail
from message import Message
from config import zeronet_directory

MESSAGE = "From: Me <me@zeromail.bit>\r\nTo: Wow <wow@zeromail.bit>\r\nSubject: Hello\r\nDate: Fri, 21 Nov 1997 09:55:06 -0600\r\nMessage-ID: zeromail0\r\n\r\nHello!\r\n"

class Mailbox(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password

		zeromail.connect(zeronet_directory, pub=user, priv=password)

	def load_messages(self):
		secrets = zeromail.update_secrets()
		messages = zeromail.update_messages(secrets)
		messages = {date: Message(int(date), data) for date, data in messages.iteritems()}
		return messages

	def messageCount(self):
		return len(self.load_messages())
	def __len__(self):
		return sum([len(message) for message in self.load_messages()])

	def getMessageIds(self):
		return [str(int(key) % 1000000) for key in self.load_messages().keys()]
	def __getitem__(self, message):
		messages = self.load_messages()
		key = [cur for cur in messages if int(cur) % 1000000 == int(message)][0]
		return messages[key]