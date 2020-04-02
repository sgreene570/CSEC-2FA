"""
SQLAlchemy model/table definitions.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HOTPEntry(Base):
    __tablename__ = "hotp"

    name = Column(String(32), primary_key=True)
    secret = Column(String(16))
    counter = Column(Integer, server_default="0")


class TOTPEntry(Base):
    __tablename__ = "totp"

    name = Column(String(32), primary_key=True)
    secret = Column(String(16))


class MailEntry(Base):
    __tablename__ = "mail"

    email = Column(String(32), primary_key=True)
    code = Column(String(12))
