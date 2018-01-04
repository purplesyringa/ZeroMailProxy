import json

def guess_private_key(zeronet_directory):
	try:
		with open(zeronet_directory + "data/users.json", "r") as f:
			users = json.loads(f.read())
			user = users[users.keys()[0]]

			zeroid = user["certs"]["zeroid.bit"]["auth_address"]

			try:
				zeromail = user["sites"]["1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27"]

				keyname = [key for key in zeromail.keys() if "encrypt_publickey" in key][0]
				publickey = zeromail[keyname]

				keyname = [key for key in zeromail.keys() if "encrypt_privatekey" in key][0]
				privatekey = zeromail[keyname]

				return (zeroid, publickey, privatekey)
			except (KeyError, TypeError):
				return (zeroid, None, None)
	except (IOError, KeyError, TypeError):
		return (None, None, None)

def guess_public_key(zeronet_directory, zeroid):
	try:
		with open(zeronet_directory + "data/1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27/data/users/" + zeroid + "/data.json") as f:
			data = json.loads(f.read())
			return data["publickey"]
	except (IOError, KeyError, TypeError):
		return None