from zeromail import ZeroMail
from message import Message
from config import zeronet_directory
import zeronet
from pop3.util import CommandError

class Mailbox(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password

		if user == "local" and password == "local":
			self.user, self.password = zeronet.guess_private_key(zeronet_directory)
			if self.user is None:
				raise CommandError("Failed to access users.json")
			elif self.password is None:
				raise CommandError("Could not find user passwords")
		elif user == "local":
			self.user, _ = zeronet.guess_private_key(zeronet_directory)
			if self.user is None:
				raise CommandError("Failed to access users.json")
		elif password == "local":
			zeroid, self.password = zeronet.guess_private_key(zeronet_directory)
			if zeroid is None:
				raise CommandError("Failed to access users.json")
			elif self.password is None:
				raise CommandError("Could not find user passwords")

		self.zeromail = ZeroMail(zeronet_directory, zeroid=self.user, priv=self.password)

	def load_messages(self):
		secrets = self.zeromail.update_secrets()
		messages = self.zeromail.update_messages(secrets)
		messages = {date: Message(int(date), data) for date, data in messages.iteritems()}
		return messages

	def messageCount(self):
		return len(self.load_messages())
	def __len__(self):
		return sum([len(message) for message in self.load_messages()])

	def getMessageIds(self):
		return [str(int(key) % 1000000) for key in self.load_messages().keys()]
	def expandMessageId(self, message):
		messages = self.load_messages()
		ids = [cur for cur in messages if int(cur) % 1000000 == int(message)]
		return ids[0] if len(ids) > 0 else None

	def __contains__(self, message):
		messages = self.load_messages()
		message_id = self.expandMessageId(message)
		return message_id is not None and message_id in messages
	def __getitem__(self, message):
		messages = self.load_messages()
		return messages[self.expandMessageId(message)]

	def pop(self, message):
		secrets = self.zeromail.update_secrets()
		self.zeromail.remove_message(secrets, self.expandMessageId(message))