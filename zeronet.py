import json, cryptlib

def guess_private_key(zeronet_directory):
	try:
		with open(zeronet_directory + "data/users.json", "r") as f:
			users = json.loads(f.read())
			user = users[users.keys()[0]]

			zeroid = user["certs"]["zeroid.bit"]["auth_address"]

			try:
				zeromail = user["sites"]["1MaiL5gfBM1cyb4a8e3iiL8L5gXmoAJu27"]

				keyname = [key for key in zeromail.keys() if "encrypt_privatekey" in key]
				if len(keyname) != 1:
					return (zeroid, None, None)
				privatekey = zeromail[keyname[0]]

				publickey = None
				keyname = [key for key in zeromail.keys() if "encrypt_publickey" in key]
				if len(keyname) == 0:
					publickey = cryptlib.private_to_public(privatekey)
				elif len(keyname) != 1:
					return (zeroid, None, None)
				else:
					publickey = zeromail[keyname[0]]

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

def sign(address, content, zeronet_directory):
	privatekey = None
	with open(zeronet_directory + "data/users.json") as f:
		users = json.loads(f.read())

		try:
			user = users[users.keys()[0]]
			privatekey = user["certs"]["zeroid.bit"]["auth_privatekey"]
		except KeyError:
			raise TypeError("Private key for zeroid.bit not found in users.json")

	from Site import Site
	site = Site(address, allow_create=False)

	site.content_manager.sign(
		inner_path=content,
		privatekey=privatekey,
		update_changed_files=True,
		remove_missing_optional=False
	)

def publish(address, content, zeronet_directory):
	# Check for lock
	from util import helper

	data_dir = zeronet_directory.replace("\\", "/") + "data"
	try:
		with helper.openLocked("%s/lock.pid" % data_dir, "w") as f:
			pass

		# Could get lock; let's run normal sitePublish then
		from src import main as zeronet_lib
		zeronet_lib.actions.sitePublish(address, inner_path=content)
	except IOError:
		# Could not get lock
		publish_socket(address, content, zeronet_directory=zeronet_directory)

def publish_socket(address, content, zeronet_directory):
	# Publish file via ZeroWebSocket

	# Find wrapper_key in sites.json
	wrapper_key = None
	with open(zeronet_directory + "data/sites.json", "r") as f:
		sites = json.loads(f.read())
		wrapper_key = sites[address]["wrapper_key"]

	# Access WebSocket
	from zerowebsocket import ZeroWebSocket
	with ZeroWebSocket(wrapper_key) as ws:
		ws.sitePublish(inner_path=content, sign=False)