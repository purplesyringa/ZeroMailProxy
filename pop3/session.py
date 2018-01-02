class Session(object):
	def __init__(self, conn):
		self.conn = conn
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
			self.err("unknown command")