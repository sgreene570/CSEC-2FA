"""
Command line interface for running the MFA demos.
"""
from functools import wraps
from getpass import getpass

import click
import sqlalchemy

import mfa_implementations.hotp as hotp
import mfa_implementations.mail as mail
import mfa_implementations.totp as totp
from supporting_code.mfa import generateSecret, renderQRCode
from supporting_code.models import Base, HOTPEntry, TOTPEntry, MailEntry

TEXT_EMAIL_MAPPING = {
    "att": "@txt.att.net",
    "tmobile": "@tmomail.net",
    "sprint": "@messaging.sprintpcs.com",
    "verizon": "@vtext.com"
}

engine = sqlalchemy.create_engine('mysql+pymysql://demo:password@localhost:3306/2fa')


def db_session(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):

        session = sqlalchemy.orm.sessionmaker(bind=engine)()

        result = func(*args, session=session, **kwargs)

        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return result

    return wrapped_function


@click.group(help=__doc__)
def cli():
    pass


@cli.command()
def init():
    """
    Initialize the application's database.
    """
    Base.metadata.create_all(engine)


@cli.command()
def drop():
    """
    Reset the application's database.
    """
    click.confirm("Are you sure?", abort=True)

    Base.metadata.drop_all(engine)


@cli.command()
@click.argument("name")
@db_session
def enroll_hotp(name, session):
    """
    Enroll an new HOTP account using the given name.

    HOTP is a counter-based one time password token.
    """
    secret = generateSecret(16)
    session.add(HOTPEntry(name=name, secret=secret))

    print("Enrollment URL for HOTP entry {}: {}".format(name, hotp.generateURL(secret)))
    print("Here are a few test OTPs:", hotp.getHOTPCode(secret, 0), hotp.getHOTPCode(secret, 1),
          hotp.getHOTPCode(secret, 2))

    print("\nEnrollment QR code:")
    renderQRCode(hotp.generateURL(secret))


@cli.command()
@click.argument("name")
@db_session
def auth_hotp(session, name):
    """
    Attempt authentication against the HOTP account with the given name.
    """
    entry = session.query(HOTPEntry).filter_by(name=name).first()
    entry.counter = hotp.run_challenge(entry.secret, entry.counter)

    session.add(entry)


@cli.command()
@click.argument("name")
@db_session
def enroll_totp(name, session):
    """
    Enroll an new TOTP account using the given name.

    TOTP is a time-based one time password token.
    """
    secret = generateSecret(16)
    session.add(TOTPEntry(name=name, secret=secret))

    print("Enrollment URL for TOTP entry {}: {}".format(name, totp.generateURL(secret)))
    print("Here is a test OTP:", totp.getTOTPCode(secret))
    print("(Valid for the next 30 seconds.)")

    print("\nEnrollment QR code:")
    renderQRCode(totp.generateURL(secret))


@cli.command()
@click.argument("name")
@db_session
def auth_totp(session, name):
    """
    Attempt authentication against the TOTP account with the given name.
    """
    entry = session.query(TOTPEntry).filter_by(name=name).first()
    totp.run_challenge(entry.secret)


@db_session
def send_mail(email, is_email, session):
    code = mail.generateCode()

    gmail_user = input("Enter a gmail address to send from: ")
    gmail_password = getpass("Enter the password for that gmail account: ")

    print("Sending OTP code " + "*" * len(code) + " to " + email + "...")
    mail.sendMail(email, gmail_user, gmail_password, code, is_email)

    session.add(MailEntry(email=email, code=code))
    print("Sent")


@cli.command()
@click.argument("email")
def send_email(email):
    """
    Generate and send an email-based one time password to the given email.
    """
    send_mail(email, True)


@db_session
def auth_mail(email, session):
    entry = session.query(MailEntry).filter_by(email=email).first()

    if entry.code == input("Enter the received code: "):
        print("Success")
        session.delete(entry)
    else:
        print("Fail")


@cli.command()
@click.argument("email")
def auth_email(email):
    """
    Attempt authentication using an email-based one time password that was sent to the given email address.
    """
    auth_mail(email)


def get_email(carrier, number):
    number = number.replace("-", "")
    assert len(number) == 10, "please use a 10 digit phone number without the country code"
    return number + TEXT_EMAIL_MAPPING[carrier]


@cli.command()
@click.argument("carrier", type=click.Choice(TEXT_EMAIL_MAPPING.keys()))
@click.argument("number")
def send_text(carrier, number):
    """
    Generate and send a text-based one time password to the given number.
    """
    send_mail(get_email(carrier, number), False)


@cli.command()
@click.argument("carrier", type=click.Choice(TEXT_EMAIL_MAPPING.keys()))
@click.argument("number")
def auth_text(carrier, number):
    """
    Attempt authentication using a text-based one time password that was sent to the given number.
    """
    auth_mail(get_email(carrier, number))


if __name__ == "__main__":
    cli()
