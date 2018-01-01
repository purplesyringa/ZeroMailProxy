import os
import sys

import Config
Config.config.disable_sslcompression = False

import CryptMessage
from lib import pyelliptic

import base64

def encrypt(text, publickey):
    encrypted = CryptMessage.encrypt(text, CryptMessage.toOpensslPublickey(publickey))
    return encrypted

def decrypt(encrypted, privatekey):
    back = CryptMessage.getEcc(privatekey).decrypt(encrypted)
    return back.decode("utf8")

# Encrypt a text using the publickey
# Return: Encrypted text and AES key using base64 encoding
def eciesEncrypt(text, publickey):
    aes_key, encrypted = encrypt(text.encode("utf8"), publickey.decode("base64"))
    return (base64.b64encode(encrypted), base64.b64encode(aes_key))

# Decrypt a text using privatekey
# Return: Decrypted text
def eciesDecrypt(encrypted_text, privatekey):
    try:
        return decrypt(encrypted_text.decode("base64"), privatekey)
    except Exception as err:
        return None

# Encrypt a text using AES
# Return: Iv, AES key, Encrypted text
def aesEncrypt(text, key=None, iv=None):
    if key:
        key = key.decode("base64")
    else:
        key = os.urandom(32)
    if iv:  # Generate new AES key if not definied
        iv = iv.decode("base64")
    else:
        iv = pyelliptic.Cipher.gen_IV('aes-256-cbc')
    if text:
        encrypted = pyelliptic.Cipher(key, iv, 1, ciphername='aes-256-cbc').ciphering(text.encode("utf8"))
    else:
        encrypted = ""
    return (base64.b64encode(key), base64.b64encode(iv), base64.b64encode(encrypted))

# Decrypt a text using AES
# Return: Decrypted text
def aesDecrypt(iv, encrypted_text, key):
    encrypted_text = encrypted_text.decode("base64")
    iv = iv.decode("base64")
    text = None
    ctx = pyelliptic.Cipher(key.decode("base64"), iv, 0, ciphername='aes-256-cbc')
    try:
        decrypted = ctx.ciphering(encrypted_text)
        if decrypted and decrypted.decode("utf8"):  # Valid text decoded
            return decrypted
    except Exception, err:
        pass
    return None