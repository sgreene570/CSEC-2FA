import secrets
import smtplib
import string
from email.message import EmailMessage

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 12


def generateCode():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def sendMail(receiver, gmail_user, gmail_password, code):
    msg = EmailMessage()
    msg["Subject"] = "Your OTP code"
    msg["From"] = gmail_user
    msg["To"] = receiver
    msg.add_header("Content-Type", "text/html")
    html = f"""\
    <html>
        <head></head>
        <body>
            <p>Here is your Second Factor Secret Code!</p>
            <mark>{code}</marK>
            </p>
        </body>
    </html>
    """
    msg.set_payload(html)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.close()
