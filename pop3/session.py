from util import debug, critical
import time

class Session(object):
	def __init__(self, conn):
		self.conn = conn
		self.state = "auth"
		self.auth = dict(user=None, password=None)
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
		self.ok("POP3 ZeroMail ready")

		while True:
			data = self.recvall()

			command = data.split(None)[0]
			args = data.split(None)[1:]

			name = "command" + command[0].upper() + command[1:].lower()
			if name in dir(self):
				getattr(self, name)(*args)
			else:
				self.err("unknown command " + command)
			time.sleep(0.5)

	def commandAuth(self):
		self.err("AUTH not supported, use USER and PASS")

	def commandCapa(self):
		self.err("CAPA not supported")

	def commandUser(self, user):
		if self.auth["user"] is not None:
			self.err("USER twice")
			return
		elif self.state != "auth":
			self.err("Current state is not AUTH")
			return

		self.auth["user"] = user
		self.ok("User OK")
	def commandPass(self, password):
		if self.auth["password"] is not None:
			self.err("PASS twice")
			return
		elif self.auth["user"] is None:
			self.err("PASS before USER")
			return
		elif self.state != "auth":
			self.err("Current state is not AUTH")
			return

		self.auth["password"] = password
		self.state = "tran"
		self.ok("Password OK")