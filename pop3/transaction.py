from util import debug, critical, ServerError, CommandError
from mailbox import Mailbox

class Transaction(object):
	def __init__(self, user, password):
		self.mailbox = Mailbox(user, password)

	def commandStat(self):
		return str(self.mailbox.messageCount()) + " " + str(len(self.mailbox))

	def commandList(self, message=None):
		if message is None:
			ids = self.mailbox.getMessageIds()
			messages = [str(message) + " " + str(len(self.mailbox[message])) for message in ids]
			messages = "\r\n".join(messages)
			return "messages follow\r\n" + messages + "\r\n."
		elif self.mailbox.hasMessage(message):
			return str(message) + " " + str(len(self.mailbox[message]))