import time
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError as sqlalchemyOpError
from psycopg2 import OperationalError as psycopg2OpError

from app.config import log
from app.config import settings
from app.models.db_models import Base


def connect_db():
    try:
        engine = create_engine(
            str(settings.DATABASE_URL),
            pool_pre_ping=True,
        )
    except Exception as e:
        log.error(e)
        log.info(f"s = {str(settings.DATABASE_URL)}")
        return
    Base.metadata.bind = engine
    return engine


def init_db() -> sessionmaker:
    connected = False
    while not connected:
        try:
            engine = connect_db()
        except (sqlalchemyOpError, psycopg2OpError):
            log.info("failed to connect to db")
            time.sleep(2)
        else:
            connected = True
            log.info("initialized db")
            session = sessionmaker(engine)
            return session
