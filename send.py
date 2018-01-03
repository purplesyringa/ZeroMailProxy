import os, sys, datetime, json

from config import zeronet_directory

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src

# Guess private/public keys
import zeronet

zeroid, privatekey = zeronet.guess_private_key(zeronet_directory)
if zeroid is None:
	print "Could not access users.json"
	zeroid = raw_input("ZeroID:")
	privatekey = raw_input("Private key:")
elif privatekey is None:
	print "ZeroID:", zeroid
	privatekey = raw_input("Private key:")
else:
	print "ZeroID:", zeroid
	print "Private key:", privatekey

from zeromail import ZeroMail
zeromail = ZeroMail(zeronet_directory, zeroid=zeroid, priv=privatekey)

print "This command-line client will send a ping message to yourself"
print "THIS WILL ONLY WORK IF YOU SEND A MESSAGE TO YOURSELF VIA ZEROMAIL BEFORE"
print ""

subject = raw_input("Subject:")

print "Body: (empty line finishes)"
body = ""
while True:
	line = raw_input()
	if line == "":
		break
	body += line + "\r\n"

to = raw_input("Your nickname (e.g. gitcenter):")

zeromail.send(zeroid, subject=subject, body=body, to=to)