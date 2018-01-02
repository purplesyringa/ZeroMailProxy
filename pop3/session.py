from util import debug, critical, ServerError, CommandError
from transaction import Transaction
import time

class Session(object):
	def __init__(self, conn):
		self.conn = conn
		self.state = "auth"
		self.auth = dict(user=None, password=None)
		self.transaction = None
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

	def ok(self, s):
		self.sendall("+OK %s" % s)
	def err(self, s):
		self.sendall("-ERR %s" % s)

	def init(self):
		debug("New session")

		self.ok("POP3 ZeroMail ready")

		while True:
			data = self.recvall()

			command = data.split(None)[0]
			args = data.split(None)[1:]

			if command.upper() == "QUIT":
				self.ok("Bye")
				debug("Session end")
				break

			name = "command" + command[0].upper() + command[1:].lower()

			try:
				if self.state == "auth":
					if name in dir(self):
						self.ok(getattr(self, name)(*args))
					else:
						raise CommandError("Unknown command " + command)
				elif self.state == "tran":
					if name in dir(self.transaction):
						self.ok(getattr(self.transaction, name)(*args))
					else:
						raise CommandError("Unknown command " + command)
			except CommandError as e:
				self.err(str(e))

			time.sleep(0.5)

	def commandAuth(self):
		raise CommandError("AUTH not supported, use USER and PASS")

	def commandCapa(self):
		raise CommandError("CAPA not supported")

	def commandUser(self, user):
		if self.auth["user"] is not None:
			raise CommandError("USER twice")
		elif self.state != "auth":
			raise CommandError("Current state is not AUTH")

		self.auth["user"] = user
		return "User OK"
	def commandPass(self, password):
		if self.auth["password"] is not None:
			raise CommandError("PASS twice")
		elif self.auth["user"] is None:
			raise CommandError("PASS before USER")
		elif self.state != "auth":
			raise CommandError("Current state is not AUTH")

		self.auth["password"] = password
		self.state = "tran"
		self.transaction = Transaction(user=self.auth["user"], password=self.auth["password"])
		return "Password OK"