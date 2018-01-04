import os, sys

zeronet_directory = "/home/ivanq/Documents/ZeroNet/" # <-- Change me depending on OS/Package settings

# Load ZeroNet plugins
os.chdir(zeronet_directory)
sys.path.insert(0, os.path.join(zeronet_directory, "plugins/CryptMessage"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src/lib"))  # External liblary directory
sys.path.insert(0, os.path.join(zeronet_directory, "src"))  # Imports relative to src
sys.path.append(zeronet_directory)  # Imports relative to ZeroNet directory