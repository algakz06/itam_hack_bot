from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


from app.models import db_models
from app.config import log


# region Users
def get_user(db: Session, tg_user_id: int) -> db_models.User | None:
    """
    help function for getting user from db by tg id,
    may be used to check if user exists, for editing information and etc
    """
    user = (
        db.query(db_models.User)
        .filter(
            db_models.User.telegram_id == tg_user_id,
        )
        .first()
    )
    if not user:
        return None
    log.info(f"User {user} was found in db")
    return user


def create_user(db: Session, tg_user_id: int, telegram_name: str, track: int, user_name: str):
    """Creating user after command /start in db"""
    db_user = db_models.User(
        telegram_id=tg_user_id,
        telegram_name=telegram_name,
        track=track,
        user_name=user_name,
        )
    db.add(db_user)
    db.commit()
    log.info(f"User {db_user} was added to db")

def create_team(db: Session, team_name: str):
    """Creating team  in db"""
    db_team = db_models.Team(
        name=team_name,
        )
    db.add(db_team)
    db.commit()
    log.info(f"Team {db_team} was added to db")

def add_user_to_team(db: Session, tg_user_id: int, team_name:str):
    """Adding user to team  in db"""
    db_user = (
        db.query(db_models.User)
        .filter(
            db_models.User.telegram_id == tg_user_id,
        )
        .first()
    )
    db_team = (
        db.query(db_models.Team)
        .filter(
            db_models.Team.name == team_name,
        )
        .first()
    )
    if not db_user:
        raise NoResultFound
    if not db_team:
        raise NoResultFound
    db_user.team = db_team.id
    db.commit()
    log.info(f"User {db_user} was added to team {db_team} in db")

# endregion