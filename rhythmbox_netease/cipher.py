from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from six import indexbytes

CIPHER = AES.new(b'rFgB&h#%2?^eDg:Q', AES.MODE_ECB)

def encrypt(plain):
    padding = 16 - len(plain) % 16
    plain += chr(padding) * padding
    return hexlify(CIPHER.encrypt(plain))

def decrypt(crypt):
    plain = CIPHER.decrypt(unhexlify(crypt))
    padding = indexbytes(plain, -1)
    return plain[:-padding]
