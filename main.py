import os, sys

from config import zeronet_directory

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src

import json

# Guess private key
zeroid = None
privatekey = None
try:
    with open(zeronet_directory + "data/users.json", "r") as f:
        users = json.loads(f.read())
        user = users[users.keys()[0]]

        zeroid = user["certs"]["zeroid.bit"]["auth_address"]

        zeromail = user["sites"]["1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27"]
        keyname = [key for key in zeromail.keys() if "encrypt_privatekey" in key][0]
        privatekey = zeromail[keyname]
except Exception as e:
    if zeroid is None:
        print "Could not load ZeroID address"
	print e
        sys.exit(1)

    privatekey = raw_input("ZeroMail private key:")

# Guess public key
publickey = None
try:
    with open(zeronet_directory + "data/1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27/data/users/" + zeroid + "/data.json") as f:
        data = json.loads(f.read())
        publickey = data["publickey"]
except:
    publickey = raw_input("ZeroMail public key:")

import zeromail
zeromail.connect(zeronet_directory, pub=publickey, priv=privatekey)

print "Updating secrets..."
secrets = zeromail.update_secrets()

print "Updating messages..."
messages = zeromail.update_messages(secrets)
for date, message in messages.items():
    print date, message