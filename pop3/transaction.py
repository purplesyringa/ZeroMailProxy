SEP = "\r\n"

from util import debug, critical, ServerError, CommandError

class Transaction(object):
	def __init__(self, user, password, Mailbox):
		self.mailbox = Mailbox(user, password)

	def commandStat(self):
		return str(self.mailbox.messageCount()) + " " + str(len(self.mailbox))

	def commandList(self, message=None):
		if message is None:
			ids = self.mailbox.getMessageIds()
			messages = [self.formatList(message) for message in ids]
			messages = SEP.join(messages)
			octets = sum([len(self.mailbox[message]) for message in ids])
			return str(len(ids)) + " messages (" + str(octets) + " octets)" + SEP + messages + SEP + "."
		elif self.mailbox.hasMessage(message):
			return self.formatList(message)
	def formatList(self, message):
		return str(message) + " " + str(len(self.mailbox[message]))

	def commandUidl(self, message=None):
		if message is None:
			ids = self.mailbox.getMessageIds()
			messages = [self.formatUidl(message) for message in ids]
			messages = SEP.join(messages)
			octets = sum([len(self.mailbox[message]) for message in ids])
			return str(len(ids)) + " messages (" + str(octets) + " octets)" + SEP + messages + SEP + "."
		elif self.mailbox.hasMessage(message):
			return self.formatUidl(message)
	def formatUidl(self, message):
		return str(message) + " " + self.mailbox[message].uidl()

	def commandRetr(self, message):
		message = int(message)

		try:
			message = self.mailbox[message]
			return "Message follows\r\n" + self.escape(str(message)) + "\r\n.\r\n"
		except KeyError:
			raise CommandError("Unknown message " + str(message))

	def escape(self, s):
		return "\r\n".join(["." + line if len(line) > 0 and line[0] == "." else line for line in s.split("\r\n")])