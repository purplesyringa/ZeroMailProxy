from util import debug

class Connection(object):
	END = "\r\n"
	def __init__(self, conn):
		self.conn = conn
	def __getattr__(self, name):
		return getattr(self.conn, name)
	def sendall(self, data, END=END):
		debug("send: %r", data)

		data += END
		self.conn.sendall(data)
	def recvall(self, END=END):
		data = []
		while True:
			chunk = self.conn.recv(4096)
			if END in chunk:
				data.append(chunk[:chunk.index(END)])
				break
			data.append(chunk)
			if len(data) > 1:
				pair = data[-2] + data[-1]
				if END in pair:
					data[-2] = pair[:pair.index(END)]
					data.pop()
					break
		debug("recv: %r", "".join(data))
		return "".join(data)