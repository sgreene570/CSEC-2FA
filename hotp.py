# HOTP Demo Code
# Python 3
# Based on http://tools.ietf.org/html/rfc4226

from common import generateSecret
import hashlib
import hmac
import struct

def main():
    # Get session secret
    secret = generateSecret(32)

    # Start counter at 0
    counter = 0

    # Program loop to show codes changing based on counter
    while True:
        print("Counter: " + str(counter))
        h = createHMAC(secret, counter)

        offset = int(h[-1:], 16)

        # Read 8 bytes
        code = h[offset:offset + 8]
        print("Full code:")
        print(code)

        code = int(code, 16) % (10 ** 6)
        print("Truncated 6 digit code:")
        print(f"{code:06d}")

        # Wait to loop
        input("Press enter for new code")
        counter += 1
        print()

def createHMAC(secret, counter):
    hasher = hmac.new(str.encode(secret), bytearray(struct.pack("f", counter)), hashlib.sha1)
    return hasher.hexdigest()

if __name__ == "__main__":
    main()
