import os, sys, datetime, json, time

# Guess private/public keys
import zeronet

zeroid, publickey, privatekey = zeronet.guess_private_key()
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
zeromail = ZeroMail(zeroid=zeroid, pub=publickey, priv=privatekey)

subject = raw_input("Subject:")

print "Body: (empty line finishes)"
body = ""
while True:
	line = raw_input()
	if line == "":
		break
	body += line + "\r\n"

to = raw_input("Recipient (e.g. gitcenter):")

zeromail.send(subject=subject, body=body, to=to, date=time.time() * 1000)