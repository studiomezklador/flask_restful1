from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import os
import uuid

def rndKey(lg=32):
    if lg >= 32:
        return uuid.uuid4().hex
    return uuid.uuid4().hex[-lg:]

BLOCK_SIZE = 32
PADDING = '#'

def _pad(data, pad_with=PADDING):
    return data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * PADDING

def encryption(secret_key, data):
    cipher = AES.new(_pad(secret_key, '@')[:32])
    return b64encode(cipher.encrypt(_pad(data)))

def decryption(secret_key, encrypted_data):
    cipher = AES.new(_pad(secret_key, '@')[:32])
    return cipher.decrypt(b64decode(encrypted_data)).rstrip(PADDING)
