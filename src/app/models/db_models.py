from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User model for SQLAlchemy"""
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    telegram_name = Column(String)
    track = Column(Integer)
    user_name = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
    team = Column(Integer, ForeignKey('teams.id'))

    def __repr__(self) -> str:
        return f"User {self.user_name} with id {self.telegram_id}"

class Team(Base):
    """Team model for SQLAlchemy"""
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
    users = relationship('User', backref='team')

    def __repr__(self) -> str:
        return f"Team {self.name} with id {self.id}"
