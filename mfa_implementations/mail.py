import secrets
import smtplib
import string
from email.message import EmailMessage

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 12


def generateCode():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def sendMail(receiver, gmail_user, gmail_password, code, is_email):
    msg = EmailMessage()
    msg["Subject"] = "Your OTP code"
    msg["From"] = gmail_user
    msg["To"] = receiver
    msg.add_header("Content-Type", "text/html")

    if is_email:
        msg.set_payload(f"""\
        <html>
            <head></head>
            <body>
                <p>Here is your Second Factor Secret Code!</p>
                <mark>{code}</marK>
                </p>
            </body>
        </html>
        """)
    else:
        msg.set_payload(code)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.close()
