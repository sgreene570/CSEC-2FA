# 2FA Demo main loop
# Python 3


from hotp import *

def main():

    # This is where our demo runner code will be
    # Complete with options for each 2fa method as well as DB saving code

    # HOTP stubbing
    hotpFlag = True

    if hotpFlag:
        counter = 0
        secret = generateSecret(16)
        renderQRCode(generateURL(secret))

        while True:
            codes = []
            for i in range(0, HOTP_WINDOW):
                codes.append(getHOTPCode(secret, counter + i))

            code = input("Enter HOTP code:\n")

            if code in codes:
                print("Success")
                counter += codes.index(code) + 1
            else:
                print("Fail")




if __name__ == "__main__":
    main()
