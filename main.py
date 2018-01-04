def formatDate(timestamp):
	date = datetime.datetime.fromtimestamp(timestamp / 1000)

	weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date.weekday()]
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][date.month - 1]
	return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, date.day, month, date.year, date.hour, date.minute, date.second)


import os, sys, datetime, json

from config import zeronet_directory

# Guess private/public keys
import zeronet

zeroid, publickey, privatekey = zeronet.guess_private_key(zeronet_directory)
if zeroid is None:
	print "Could not access users.json"
	zeroid = raw_input("ZeroID:")
	publickey = raw_input("Public key:")
	privatekey = raw_input("Private key:")
elif publickey is None or privatekey is None:
	print "ZeroID:", zeroid
	publickey = raw_input("Public key:")
	privatekey = raw_input("Private key:")
else:
	print "ZeroID:", zeroid
	print "Public key:", publickey
	print "Private key:", privatekey

from zeromail import ZeroMail
zeromail = ZeroMail(zeronet_directory, zeroid=zeroid, pub=publickey, priv=privatekey)

print "Updating secrets..."
secrets = zeromail.update_secrets()

print "Updating messages..."
messages = zeromail.update_messages(secrets)
for date, message in messages.items():
	data = json.loads(message["raw"])
	print "Date: " + formatDate(int(date))
	print "From: " + message["cert_user_id"]
	print "To: " + data["to"]
	print "Subject: " + data["subject"]
	print ""
	print data["body"]
	print ""
	print "---"
	print ""