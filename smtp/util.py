def debug(s, *args):
	if isinstance(s, basestring):
		print "[smtp] [debug   ] %s" % (s % args)
	else:
		print "[smtp] [debug   ] %s" % s

def critical(s, *args):
	if isinstance(s, basestring):
		print "[smtp] [critical] %s" % (s % args)
	else:
		print "[smtp] [critical] %s" % s


class ServerError(Exception):
	pass
class CommandError(Exception):
	pass