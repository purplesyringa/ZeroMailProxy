import hashlib, json, datetime, markdown, array

class Message(object):
	def __init__(self, date, data):
		self.raw = data["raw"]

		raw = json.loads(self.raw)

		self.date = date
		self.body = raw["body"]
		self.to = raw["to"]
		self.from_ = data["cert_user_id"]
		self.subject = raw["subject"]

		bts = [ord(char) for char in self.body]
		bts = array.array("B", bts).tostring().decode("utf8")
		self.body = self.from_markdown(bts)

	def from_markdown(self, text):
		return markdown.markdown(text)

	def __len__(self):
		return len(unicode(self))

	def headers(self):
		return (
			u"From: " + self.from_ + u"\r\n" +
			u"To: " + self.to + u"\r\n" +
			u"Subject: " + self.subject + u"\r\n" +
			u"Date: " + self.formatDate(self.date) + u"\r\n"
			u"Content-Type: text/html; charset=utf-8\r\n"
		)

	def __str__(self):
		return unicode(self).encode("utf-8")
	def __unicode__(self):
		try:
			self.headers() + u"\r\n" + self.body
		except UnicodeEncodeError as e:
			print self.body

		try:
			return self.headers() + u"\r\n" + self.body
		except UnicodeEncodeError as e:
			pass

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
		md5.update(str(self.date) + "|")
		md5.update(self.raw.encode("utf-8"))
		return md5.hexdigest() + "|v3"