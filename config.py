import os, sys

zeronet_directory = "C:\\Users\\Ivanq\\Documents\\ZeroNet\\" # <-- Change me depending on OS/Package settings
data_directory = "C:\\Users\\Ivanq\\Documents\\ZeroNet\\data\\" # <-- Change me depending on OS/Package settings

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src
sys.path.append(zeronet_directory)  # Imports relative to ZeroNet directory

# Set ZeroNet config

import Config
Config.config.debug = False
Config.config.debug_gevent = False
Config.config.use_tempfiles = False
Config.config.data_dir = data_directory.replace("\\", "/")
Config.config.db_mode = "speed"
Config.config.language = "en"
Config.config.fileserver_port = "15441"
Config.config.homepage = "1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
Config.config.disable_db = False
Config.config.verbose = False
Config.config.size_limit = 10
Config.config.fileserver_ip = "127.0.0.1"
Config.config.bit_resolver = "1Name2NXVi1RDPDgf5617UoW7xA6YrhM9F"
Config.config.tor = "disabled"
Config.config.ip_local = "127.0.0.1"
Config.config.ip_external = None
Config.config.disable_encryption = False
Config.config.trackers_file = False