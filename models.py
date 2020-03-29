"""
SQLAlchemy model/table definitions.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class HOTPEntry(Base):
    __tablename__ = 'htop'

    name = Column(String(32), primary_key=True)
    secret = Column(String(16))
    counter = Column(Integer, server_default="0")
