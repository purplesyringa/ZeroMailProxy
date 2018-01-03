from util import debug, critical, ServerError, CommandError
from transaction import Transaction
import time, base64

class Session(object):
	def __init__(self, conn, Mailbox):
		self.conn = conn
		self.raw_handler = None
		self.Mailbox = Mailbox
		self.transaction = None
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

	def ok(self, s):
		self.status(250, s)
	def ok_(self, s):
		self.status_(250, s)
	def status(self, status, s):
		self.sendall("%s %s" % (status, s))
	def status_(self, status, s):
		self.sendall("%s-%s" % (status, s))

	def init(self):
		debug("New session")

		self.status(220, "SMTP server ready")
		self.state = "awaitEhlo"

		while True:
			data = self.recvall()

			handler = self.transaction if self.transaction is not None else self

			if handler.raw_handler is None:
				command = data.split(None)[0]
				args = data.split(None)[1:]

				if command.upper() == "QUIT":
					self.ok("Bye")
					break

				name = "command" + command[0].upper() + command[1:].lower()

				try:
					if name in dir(handler):
						getattr(handler, name)(*args)
					else:
						self.status(500, "Unknown command")
				except AssertionError as e:
					self.status(503, "bad sequence of commands")
			else:
				getattr(handler, handler.raw_handler)(data)

	def commandEhlo(self, server):
		self.ok_("SMTP server here")
		self.ok("AUTH PLAIN")

	def commandAuth(self, type, data=None):
		if type.upper() != "PLAIN":
			self.status(504, "Only AUTH PLAIN supported")
			return

		if data is None:
			self.raw_handler = "handleAuth"
			self.status(334, "Waiting AUTH data")
		else:
			self.handleAuth(data)
	def handleAuth(self, data):
		if data == "*":
			self.status(501, "Think before doing next time")
			return

		try:
			data = base64.b64decode(data)
		except:
			self.status(501, "Invalid Base64")

		self.auth(data)
		self.status(235, "Welcome")

	def auth(self, data):
		print [format(ord(char), "02x") for char in data]
		zid = data[:data.index("\x00")]
		login = data[data.index("\x00")+1:data.rindex("\x00")]
		password = data[data.rindex("\x00")+1:]

		self.transaction = Transaction(self.conn)

	def commandMail(self):
		self.status(530, "Auth required")
	def commandRcpt(self):
		self.status(530, "Auth required")
	def commandData(self):
		self.status(530, "Auth required")
