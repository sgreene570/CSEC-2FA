import os
import secrets
import smtplib
import string
from email.message import EmailMessage

# Get credentials from term env
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
CODE_LENGTH = 12

def main():
    # Generate mail temporary code
    # Use python secrets instead of random for security
    alphabet = string.ascii_letters + string.digits
    code = "".join(secrets.choice(alphabet) for i in range(CODE_LENGTH))
    receiver = input("Enter receiver address:\n")
    print("Sending OTP code " + '*' * len(code) + " to " + receiver)
    success = sendMail(receiver, code)
    # If email failed, exit program
    if not success:
        return
    print("Message sent")
    check = input("Enter received code:\n")
    if(check == code):
        print("Success")
    else:
        print("Failure")

def sendMail(receiver, code):
    sentFrom = GMAIL_USER
    msg = EmailMessage()
    msg["Subject"] = "Your OTP code"
    msg["From"] = GMAIL_USER
    msg["to"] = receiver
    msg.set_content(code)
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.close()
    except Exception as e:
        print(e)
        return False

    return True

if __name__ == "__main__":
    main()
