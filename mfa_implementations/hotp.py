"""
Standard HOTP implementation based on http://tools.ietf.org/html/rfc4226.
"""
from supporting_code.mfa import *
import hashlib
import hmac

HOTP_WINDOW = 10


def run_challenge(secret, counter):
    while True:
        codes = []
        for i in range(0, HOTP_WINDOW):
            codes.append(getHOTPCode(secret, counter + i))

        code = input("Enter HOTP code (or press enter to exit): ")

        if not code:
            return counter

        if code in codes:
            print("Success")
            counter += codes.index(code) + 1
        else:
            print("Fail")


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
