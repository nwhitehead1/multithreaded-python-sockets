from Crypto.PublicKey import RSA
from Crypto import Random

# Return tuple of (private, public)
def keyGen():
    modulusLen = 1024
    rand = Random.new().read
    privateKey = RSA.generate(modulusLen, rand)
    publicKey = privateKey.publickey()
    return privateKey, publicKey

def encrypt(raw: bytes, publicKey: RSA._RSAobj):
    return publicKey.encrypt(raw, 32)[0]

def decrypt(encoded: bytes, privateKey: RSA._RSAobj):
    return privateKey.decrypt(encoded)

def stringToKey(keyString):
    return RSA.importKey(keyString)

def keyToBytes(keyObj: RSA._RSAobj):
    return keyObj.exportKey()