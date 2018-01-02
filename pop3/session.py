from util import debug, critical
import time

class Session(object):
	def __init__(self, conn):
		self.conn = conn
		self.state = "auth"
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

	def commandAuth():
		debug("Open AUTH")