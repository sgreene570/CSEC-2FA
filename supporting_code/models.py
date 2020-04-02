"""
SQLAlchemy model/table definitions.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class HOTPEntry(Base):
    __tablename__ = 'hotp'

    name = Column(String(32), primary_key=True)
    secret = Column(String(16))
    counter = Column(Integer, server_default="0")


class TOTPEntry(Base):
    __tablename__ = 'totp'

    name = Column(String(32), primary_key=True)
    secret = Column(String(16))
