from util import debug, critical, ServerError, CommandError
from transaction import Transaction
import time

class Session(object):
	def __init__(self, conn, Mailbox):
		self.conn = conn
		self.state = None
		self.raw_handler = None
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

			if self.raw_handler is None:
				command = data.split(None)[0]
				args = data.split(None)[1:]

				if command.upper() == "QUIT":
					self.ok("Bye")
					break

				name = "command" + command[0].upper() + command[1:].lower()

				try:
					if name in dir(self):
						getattr(self, name)(*args)
				except AssertionError as e:
					self.status(503, "bad sequence of commands")
			else:
				getattr(self, self.raw_handler)(data)

	def commandEhlo(self, server):
		assert self.state == "awaitEhlo"

		self.state = "awaitMail"
		self.ok("SMTP server here")

	def commandMail(self, *args):
		assert self.state == "awaitMail"

		args = self.parseColon(args)
		self.from_ = args["FROM"][1:-1]

		self.state = "awaitRcpt"
		self.ok("Ready to accept recipients")

	def commandRcpt(self, *args):
		assert self.state == "awaitRcpt"

		args = self.parseColon(args)
		self.to = args["TO"][1:-1]

		self.state = "awaitRcpt"
		self.ok(self.to + " ok")

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
		self.ok("Message sent")

		print ""
		print ""
		print "From: " + from_
		print "To: " + to
		print ""
		print data
		print ""
		print ""

	def parseColon(self, args):
		res = dict()
		for arg in args:
			key = arg.split(":", 1)[0]
			value = arg.split(":", 1)[1]
			res[key.upper()] = value
		return res