from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


from app.models import db_models, models
from app.config import log


# region Users
def get_user(db: Session, tg_user_id: int) -> models.User | None:
    """
    help function for getting user from db by tg id,
    may be used to check if user exists, for editing information and etc
    """
    user = (
        db.query(db_models.Users)
        .filter(
            db_models.Users.tg_id == tg_user_id,
        )
        .first()
    )
    if not user:
        return None
    log.info(f"User {user} was found in db")
    return models.User.from_orm(user)


def add_user_to_db(db: Session, tg_user_id: int):
    """adding user after command /start to db"""
    db_user = db_models.Users(tg_id=tg_user_id)
    db.add(db_user)
    db.commit()
    log.info(f"User {db_user} was added to db")


# endregion


# region Notion
def add_notion_token(
    db: Session,
    tg_user_id: int,
    token: Optional[str] = "",
):
    """adding notion token to db"""
    db_user = (
        db.query(db_models.Users)
        .filter(
            db_models.Users.tg_id == tg_user_id,
        )
        .first()
    )
    if not db_user:
        raise NoResultFound
    db_user.notion_token = token
    db.commit()
    log.info(f"User {db_user} was added notion token to db")


def add_notion_db(db: Session, tg_user_id: int, db_id: str, db_name: str):
    """adding notion db to db"""
    db_user = (
        db.query(db_models.Users)
        .filter(
            db_models.Users.tg_id == tg_user_id,
        )
        .first()
    )

    if not db_user:
        raise NoResultFound

    db_db = db_models.Databases(
        db_id=db_id,
        db_name=db_name,
        user_id=db_user.id,
    )

    db.add(db_db)
    db.commit()

    log.info(f"User {db_user} added notion db: {db_id} to db")


# endregion
