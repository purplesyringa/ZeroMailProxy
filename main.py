import os, sys

zeronet_directory = "C:\\Users\\Ivanq\\Documents\\ZeroNet\\" # <-- Change me depending on OS/Package settings

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src

import zeromail

zeromail.connect(zeronet_directory, pub="", priv="")

print "Loading secrets..."
secrets = zeromail.get_secrets()

print "Loading messages..."
messages = zeromail.get_messages(secrets)
for message in messages:
    print message