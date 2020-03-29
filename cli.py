"""
Command line interface for running the MFA demos.
"""
from functools import wraps
import click
import sqlalchemy
from supporting_code.models import Base, HOTPEntry
from supporting_code.mfa import generateSecret, renderQRCode
import mfa_implementations.hotp as hotp

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


if __name__ == '__main__':
    cli()
