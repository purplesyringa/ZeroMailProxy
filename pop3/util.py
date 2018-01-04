def debug(s, *args):
	if isinstance(s, basestring):
		print "[pop3] [debug   ] %s" % (s % args)
	else:
		print "[pop3] [debug   ] %s" % s

def critical(s, *args):
	if isinstance(s, basestring):
		print "[pop3] [critical] %s" % (s % args)
	else:
		print "[pop3] [critical] %s" % s


class ServerError(Exception):
	pass
class CommandError(Exception):
	pass