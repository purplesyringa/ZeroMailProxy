import hashlib, json, datetime

class Message(object):
	def __init__(self, date, data):
		self.raw = data["raw"]

		raw = json.loads(self.raw)

		self.date = date
		self.body = raw["body"]
		self.to = raw["to"]
		self.from_ = data["cert_user_id"]
		self.subject = raw["subject"]

	def __len__(self):
		return len(str(self))

	def headers(self):
		return (
			"From: " + self.from_ + "\r\n" +
			"To: " + self.to + "\r\n" +
			"Subject: " + self.subject + "\r\n" +
			"Date: " + self.formatDate(self.date) + "\r\n"
		)

	def __str__(self):
		return self.headers() + "\r\n" + self.body

	def top(self, lines):
		top = "\r\n".join(self.body.split("\r\n")[:lines])

		return self.headers() + "\r\n" + top

	def formatDate(self, timestamp):
		date = datetime.datetime.fromtimestamp(timestamp / 1000)

		weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date.weekday()]
		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][date.month - 1]
		return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, date.day, month, date.year, date.hour, date.minute, date.second)

	def uidl(self):
		md5 = hashlib.md5()
		md5.update(str(self.date) + "|" + self.raw)
		return md5.hexdigest() + "|v2"