"""
Command line interface for running the MFA demos.
"""
from functools import wraps
import click
import sqlalchemy
from models import Base, User

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
    Base.metadata.create_all(engine)


@cli.command()
def drop():
    click.confirm("Are you sure?", abort=True)

    Base.metadata.drop_all(engine)


@cli.command()
@click.argument("username")
@db_session
def add(username, session):
    user = User(name=username)
    session.add(user)


@cli.command()
@db_session
def list(session):
    for user in session.query(User).all():
        print(user)


if __name__ == '__main__':
    cli()
