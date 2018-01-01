import os, sys

zeronet_directory = "C:\\Users\\Ivanq\\Documents\\ZeroNet\\" # <-- Change me depending on OS/Package settings

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src

import json

privatekey = None
try:
    with open(zeronet_directory + "data/users.json", "r") as f:
        users = json.loads(f.read())
        user = users[users.keys()[0]]
        zeromail = user["sites"]["1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27"]
        keyname = [key for key in zeromail.keys() if "encrypt_privatekey" in key][0]
        privatekey = zeromail[keyname]
except:
    privatekey = raw_input("ZeroMail private key:")

import zeromail
zeromail.connect(zeronet_directory, pub="", priv=privatekey)

print "Loading secrets..."
secrets = zeromail.get_secrets()

print "Loading messages..."
messages = zeromail.get_messages(secrets)
for message in messages:
    print message