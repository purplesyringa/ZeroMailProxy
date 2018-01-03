from util import CommandError

class Transaction(object):
	def __init__(self, user, password, Mailbox, conn):
		self.conn = conn

		try:
			self.mailbox = Mailbox(user, password)
		except CommandError as e:
			self.status(535, str(e))
			return

		self.raw_handler = None
		self.state = "awaitMail"

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


	def commandMail(self, *args):
		assert self.state == "awaitMail"

		args = self.parseColon(args)
		self.from_ = args["FROM"][1:-1]
		self.to = []
		self.data = ""

		self.state = "awaitRcpt"
		self.ok("Ready to accept recipients")

	def commandRcpt(self, *args):
		assert self.state == "awaitRcpt"

		args = self.parseColon(args)
		self.to.append(args["TO"][1:-1])

		self.state = "awaitRcpt"
		self.ok(args["TO"][1:-1] + " ok")

	def commandData(self, *args):
		assert self.state == "awaitRcpt"
		self.raw_handler = "handleData"
		self.data = ""
		self.status(354, "Intermediate reply")
	def handleData(self, data):
		if data == "":
			self.data += "\r\n"
		elif data == ".":
			self.state = "awaitRcpt"
			self.send(self.from_, self.to, self.data)
			self.from_ = ""
			self.to = ""
			self.data = ""
			self.raw_handler = None
		elif data[0] == ".":
			self.data += data[1:] + "\r\n"
		else:
			self.data += data + "\r\n"
	def send(self, from_, to, data):
		try:
			self.mailbox.send(from_, to, data)
			self.ok("Sent")
			self.state = "awaitMail"
		except CommandError as e:
			self.status(450, str(e))

	def commandRset(self):
		self.state = "awaitMail"
		self.ok("OK")

	def commandNoop(self):
		self.ok("OK")

	def parseColon(self, args):
		res = dict()
		for arg in args:
			key = arg.split(":", 1)[0]
			value = arg.split(":", 1)[1]
			res[key.upper()] = value
		return res