def debug(s, *args):
	if isinstance(s, basestring):
		print "[debug   ] %s" % (s % args)
	else:
		print "[debug   ] %s" % s

def critical(s, *args):
	if isinstance(s, basestring):
		print "[critical] %s" % (s % args)
	else:
		print "[critical] %s" % s