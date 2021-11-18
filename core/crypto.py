import os
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:
    
    def __init__(self, key):
        self.key = base64.b64decode(key)
        self.bs  = AES.block_size
        
    def pad(self, s):
        pads = s + (self.bs - len(s) % self.bs) * "\x00"
        return pads

    def unpad(self, s):
        s = s.decode('utf-8')
        return s.rstrip('\x00')

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8")))
    
    def decrypt(self,enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_p = cipher.decrypt(enc[16:])
        return self.unpad(plain_p)

def key_init():
    key = base64.b64encode(os.urandom(32))
    return key.decode()

def ENCRYPT(PLAIN, KEY):
    c = AESCipher(KEY)
    enc = c.encrypt(PLAIN)
    return enc.decode()

def DECRYPT(ENC, KEY):
    c = AESCipher(KEY)
    dec = c.decrypt(ENC)
    return dec