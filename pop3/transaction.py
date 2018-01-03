SEP = "\r\n"

from util import debug, critical, ServerError, CommandError

class Transaction(object):
	def __init__(self, user, password, Mailbox):
		self.mailbox = Mailbox(user, password)
		self.to_delete = []
	def finish(self):
		errs = 0
		for message in self.to_delete:
			try:
				self.mailbox.pop(message)
			except KeyError:
				errs += 1

		if errs == 0:
			return "Transaction finished"
		else:
			raise CommandError("Finished with " + str(errs) + " delete errors")

	def commandStat(self):
		return str(self.mailbox.messageCount()) + " " + str(len(self.mailbox))

	def commandList(self, message=None):
		if message is None:
			ids = self.mailbox.getMessageIds()
			messages = [self.formatList(message) for message in ids]
			messages = SEP.join(messages)
			octets = sum([len(self.mailbox[message]) for message in ids])
			return str(len(ids)) + " messages (" + str(octets) + " octets)" + SEP + messages + SEP + "."
		elif message in self.mailbox:
			return self.formatList(message)
		else:
			raise CommandError("Unknown message")
	def formatList(self, message):
		return str(message) + " " + str(len(self.mailbox[message]))

	def commandUidl(self, message=None):
		if message is None:
			ids = self.mailbox.getMessageIds()
			messages = [self.formatUidl(message) for message in ids]
			messages = SEP.join(messages)
			octets = sum([len(self.mailbox[message]) for message in ids])
			return str(len(ids)) + " messages (" + str(octets) + " octets)" + SEP + messages + SEP + "."
		elif message in self.mailbox:
			return self.formatUidl(message)
		else:
			raise CommandError("Unknown message")
	def formatUidl(self, message):
		return str(message) + " " + self.mailbox[message].uidl()

	def commandRetr(self, message):
		message = int(message)

		try:
			message = self.mailbox[message]
			return "Message follows\r\n" + self.escape(str(message)) + "\r\n."
		except KeyError:
			raise CommandError("Unknown message " + str(message))
	def commandTop(self, message, lines):
		message = int(message)
		lines = int(lines)

		try:
			message = self.mailbox[message]
			return "Message top follows\r\n" + self.escape(message.top(lines)) + "\r\n."
		except KeyError:
			raise CommandError("Unknown message " + str(message))

	def commandDele(self, message):
		message = int(message)
		self.to_delete.append(message)
		return "Okay"
	def commandRset(self):
		self.to_delete = []
		return "Think before doing next time"

	def commandNoop(self):
		return "Ping-pong"

	def escape(self, s):
		return "\r\n".join(["." + line if len(line) > 0 and line[0] == "." else line for line in s.split("\r\n")])