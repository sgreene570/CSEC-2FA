# OTP Demo Code
# Python 3
# Based on https://tools.ietf.org/html/rfc6238

from common import *
from datetime import datetime
import base64
import hmac
import hashlib
import struct
import time

WINDOW = 30

def main():
    # Get session secret
    secret = generateSecret(16)

    print(generateURL(secret))
    renderQRCode(generateURL(secret))

    while True:
        t = getUnixTime()
        print(t)

        h = createHMAC(secret, t)

        offset = int(h[-1:], 16)

        print("Full code:")

        code = h[offset:offset + 8]
        code = int(code, 16) % (10 ** 6)
        print("Truncated 6 digit code:")
        print(f"{code:06d}")

        # Wait to loop
        input("Press enter for new code")
        print()

def getUnixTime():
    return int(time.time() / WINDOW)

def createHMAC(secret, time):
    hasher = hmac.new(str.encode(secret), bytearray(struct.pack("d", time)), hashlib.sha1)
    return hasher.hexdigest()

def generateURL(secret):
    return "otpauth://totp/Test%20App:test%40test.com?secret=" + \
    base64.b32encode(bytearray(secret, 'ascii')).decode().replace('=', '') + \
    "&issuer=Test%20App"

if __name__ == "__main__":
    main()
