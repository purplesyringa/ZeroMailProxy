from util import debug, critical, ServerError, CommandError
from transaction import Transaction
import time

class Session(object):
	def __init__(self, conn, Mailbox):
		self.conn = conn
		self.state = None
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

	def ok(self, s):
		self.status(250, s)
	def status(self, status, s):
		self.sendall("%s %s" % (status, s))

	def init(self):
		debug("New session")

		self.status(220, "SMTP server ready")
		self.state = "awaitEhlo"

		while True:
			data = self.recvall()

			command = data.split(None)[0]
			args = data.split(None)[1:]

			name = "command" + command[0].upper() + command[1:].lower()

			try:
				if name in dir(self):
					getattr(self, name)(*args)
			except AssertionError as e:
				self.status(503, "bad sequence of commands")

	def commandEhlo(self, server):
		assert self.state == "awaitEhlo"

		self.state = "awaitMail"
		self.ok("SMTP server here")