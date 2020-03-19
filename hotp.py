# HOTP Demo Code
# Python 3
# Based on http://tools.ietf.org/html/rfc4226

from common import *
import hashlib
import hmac
import struct

HOTP_WINDOW = 10

def main():
    # Get session secret
    secret = generateSecret(16)

    # Start counter at 0
    counter = 0

    url = generateURL(secret)
    renderQRCode(url)

    # Program loop to generate HOTP codes of window size
    while True:
        codes = []
        for i in range(0, HOTP_WINDOW):
            codes.append(getHOTPCode(secret, counter + i))

        print(codes)
        input("Press enter for new code set")
        print()

        counter += 1

def getHOTPCode(secret, counter):
    h = createHMAC(secret, counter)
    # Get last nibble of the hmac hash
    offset = h[-1] & 0xf

    code = ((h[offset] & 0x7f) << 24 |
            (h[offset + 1] & 0xff) << 16 |
            (h[offset + 2] & 0xff) << 8 |
            (h[offset + 3] & 0xff))

    # Modulo to find 6 digit code
    code = code % (10 ** 6)

    return f"{code:06d}"

def createHMAC(secret, time):
    hasher = hmac.new(bytearray(secret, 'ascii'), getBytesFromInt(time), hashlib.sha1)
    return bytearray(hasher.digest())

def generateURL(secret):
    return "otpauth://hotp/Test%20App:test%40test.com?secret=" + \
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
