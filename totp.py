# OTP Demo Code
# Python 3

from datetime import datetime
import hmac
import hashlib
import random
import string
import struct
import time

def generateSecret(length):
    content = string.ascii_letters + string.digits
    return ''.join(random.choice(content) for i in range(length))

def getDateTime():
    return datetime.now()

def getUnixTime():
    return time.time()

def createHMAC(secret, time):
    hasher = hmac.new(str.encode(secret), bytearray(struct.pack("f", time)), hashlib.sha1)
    return hasher.hexdigest()


secret = generateSecret(32)

t = getUnixTime()

h = createHMAC(secret, t)

offset = int(h[-1:], 16)

print(h)
# Read 8 bytes
code = h[offset:offset + 8]
print(code)

code = int(code, 16) % (10 ** 6)
print(code)





