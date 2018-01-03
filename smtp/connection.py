from util import debug

class Connection(object):
	END = "\r\n"
	def __init__(self, conn):
		self.conn = conn
		self.awaiting = []
		self.tmpAwaiting = ""

	def __getattr__(self, name):
		return getattr(self.conn, name)

	def sendall(self, data, END=END):
		debug("send: %r", data)

		data += END
		self.conn.sendall(data)

	def recvall(self, END=END):
		if len(self.awaiting) > 0:
			data = self.awaiting.pop(0)
			debug("recv: %r", "".join(data))
			return data

		while True:
			chunk = self.conn.recv(4096)
			self.tmpAwaiting += chunk
			if END in self.tmpAwaiting:
				while END in self.tmpAwaiting:
					self.awaiting.append(self.tmpAwaiting[:self.tmpAwaiting.index(END)])
					self.tmpAwaiting = self.tmpAwaiting[self.tmpAwaiting.index(END) + len(END):]
				break

		if len(self.awaiting) > 0:
			data = self.awaiting.pop(0)
			debug("recv: %r", "".join(data))
			return data

		return None