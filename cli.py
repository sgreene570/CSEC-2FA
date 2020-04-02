"""
Command line interface for running the MFA demos.
"""
from functools import wraps
import click
import sqlalchemy
from supporting_code.models import Base, HOTPEntry, TOTPEntry
from supporting_code.mfa import generateSecret, renderQRCode
import mfa_implementations.hotp as hotp
import mfa_implementations.totp as totp

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


if __name__ == "__main__":
    cli()
