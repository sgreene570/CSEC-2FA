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
        t = getUnixTimeIntervals()

        h = createHMAC(secret, t)

        # Get last nibble of the hmac hash
        offset = h[-1] & 0xf

        code = ((h[offset] & 0x7f) << 24 |
                (h[offset + 1] & 0xff) << 16 |
                (h[offset + 2] & 0xff) << 8 |
                (h[offset + 3] & 0xff))

        code = code % (10 ** 6)
        print("Truncated 6 digit code:")
        print(f"{code:06d}")

        # Wait to loop
        input("Press enter for new code:\n")

def getUnixTimeIntervals():
    # Return the number of WINDOW periods at this current time
    # Use int() to truncate automatically
    return int(time.time() / WINDOW)

def createHMAC(secret, time):
    hasher = hmac.new(bytearray(secret, 'ascii'), getBytesFromInt(time), hashlib.sha1)
    return bytearray(hasher.digest())

def generateURL(secret):
    return "otpauth://totp/Test%20App:test%40test.com?secret=" + \
    b32EncodeString(secret).decode().replace('=', '') + \
    "&issuer=Test%20App"

def getBytesFromInt(i, padding=8):
    result = bytearray()
    while i != 0:
        result.append(i & 0xff)
        i >>= 8
    return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

if __name__ == "__main__":
    main()
