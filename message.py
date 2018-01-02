import hashlib, json, datetime

class Message(object):
	def __init__(self, date, data):
		self.raw = data

		data = json.loads(data)

		self.date = date
		self.body = data["body"]
		self.to = data["to"]
		self.subject = data["subject"]

	def __len__(self):
		return len(str(self))

	def __str__(self):
		return (
			"From: anonymous@zeromail.bit\r\n" +
			"To: " + self.to + "\r\n" +
			"Subject: " + self.subject + "\r\n" +
			"Date: " + self.formatDate(self.date) + "\r\n" +
			"\r\n" +
			self.body
		)

	def formatDate(self, timestamp):
		date = datetime.datetime.fromtimestamp(timestamp / 1000)

		weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date.weekday()]
		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][date.month - 1]
		return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, date.day, month, date.year, date.hour, date.minute, date.second)

	def uidl(self):
		md5 = hashlib.md5()
		md5.update(str(self.date) + "|" + self.raw)
		return md5.hexdigest()