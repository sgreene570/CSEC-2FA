"""
Demo of the OTP library. This library implements the TOTP standard used by Google Authenticator-compatible OTP systems.
See the doc link below for details.

Also includes support for counter-based OTPs and the Google Authenticator URI standard.

Requires pyotp:
    pip install pyotp

https://pyotp.readthedocs.io/en/latest/
"""

import pyotp

print("Time-based OTP demo")

token = pyotp.random_base32()

print("Here's your token:", token)

totp = pyotp.TOTP(token)

print("OTPs are valid for 30 seconds.")

while True:
    print()
    print("OTP generated using that token and the current time:", totp.now())
    otp_in = input("Enter an OTP to verify: ")

    if otp_in:
        print("Result:", totp.verify(otp_in))
    else:
        break
