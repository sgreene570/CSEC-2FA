# MFA project common utils
# Python 3

import pyqrcode
import secrets
import string

def generateSecret(length):
    content = string.ascii_letters + string.digits
    return ''.join(secrets.choice(content) for i in range(length))

def renderQRCode(url):
    url = pyqrcode.create(url)
    print(url.terminal(quiet_zone=1))

