"""
Utilities for the MFA implementations.
"""
import base64
import pyqrcode
import secrets
import string


def generateSecret(length):
    content = string.ascii_letters + string.digits
    return ''.join(secrets.choice(content) for i in range(length))


def renderQRCode(url):
    url = pyqrcode.create(url)
    print(url.terminal(quiet_zone=1))


def b32EncodeString(s):
    return base64.b32encode(bytearray(s, 'ascii'))
