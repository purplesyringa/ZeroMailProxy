from util import debug, critical, ServerError, CommandError

class Transaction(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password