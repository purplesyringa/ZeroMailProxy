import os, sys, datetime, json

from config import zeronet_directory

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src

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

print "This command-line client will send a message"
print "THIS WILL ONLY WORK IF YOU SENT A MESSAGE TO RECIPIENT VIA ZEROMAIL BEFORE"
print ""

subject = raw_input("Subject:")

print "Body: (empty line finishes)"
body = ""
while True:
	line = raw_input()
	if line == "":
		break
	body += line + "\r\n"

to = raw_input("Recipient (e.g. gitcenter):")

zeromail.send(subject=subject, body=body, to=to)