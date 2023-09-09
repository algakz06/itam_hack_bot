from sqlalchemy import create_engine, func, join
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import OperationalError as sqlalchemyOpError
from psycopg2 import OperationalError as psycopg2OpError

from app.config import settings
from app.models.db_models import Base
from app.models import db_models

from time import sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Optional
from sqlalchemy.exc import OperationalError as sqlalchemyOpError
from psycopg2 import OperationalError as psycopg2OpError

class DBManager:
    def __init__(self, log):
        self.pg_user = settings.POSTGRES_USER
        self.pg_pass = settings.POSTGRES_PASSWORD
        self.pg_host = settings.POSTGRES_HOST
        self.pg_port = settings.POSTGRES_PORT
        self.pg_db = settings.POSTGRES_DB
        self.log = log
        connected = False
        while not connected:
            try:
                self._connect()
            except (sqlalchemyOpError, psycopg2OpError):
                sleep(2)
            else:
                connected = True
        self._recreate_tables()

    def __del__(self):
        """Close the database connection when the object is destroyed"""
        self._close()

    # region Connection setup
    def _connect(self) -> None:
        """Connect to the postgresql database"""
        self.engine = create_engine(f'postgresql+psycopg2://{self.pg_user}:{self.pg_pass}@{self.pg_host}:{self.pg_port}\
/{self.pg_db}',
                                    pool_pre_ping=True)
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def _close(self) -> None:
        """Closes the database connection"""
        self.session.close_all()

    def _recreate_tables(self) -> None:  # Important: Do not use in production!
        """Removes and recreates all tables in DB"""
    #     Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        # region Users
    def get_user(self, tg_user_id: int) -> db_models.User | None:
        """
        help function for getting user from db by tg id,
        may be used to check if user exists, for editing information and etc
        """
        user = (
            self.session.query(db_models.User)
            .filter(
                db_models.User.telegram_id == tg_user_id,
            )
            .first()
        )
        if not user:
            return None
        self.log.info(f"User {user} was found in db")
        return user


    def create_user(
        self,
        tg_user_id: int,
        telegram_name: str,
        track: int,
        type_of_presense: str,
        user_name: str,
        team: Optional[str] = None,
        university_group: Optional[str] = None,
        specialty: Optional[str] = None,
        ):
        """Creating user after command /start in db"""
        db_user = db_models.User(
            telegram_id=tg_user_id,
            telegram_name=telegram_name,
            team=team,
            type_of_presense=type_of_presense,
            track=track,
            specialty=specialty,
            user_name=user_name,
            university_group=university_group,
            )
        self.session.add(db_user)
        self.session.commit()
        self.log.info(f"User {db_user} was added to db")

    def create_team(self, team_name: str):
        """Creating team  in db"""
        db_team = db_models.Team(
            name=team_name,
            )
        self.session.add(db_team)
        self.session.commit()
        self.log.info(f"Team {db_team} was added to db")

    def add_user_to_team(self, tg_user_id: int, team_name:str):
        """Adding user to team  in db"""
        db_user = (
            self.session.query(db_models.User)
            .filter(
                db_models.User.telegram_id == tg_user_id,
            )
            .first()
        )
        db_team = (
            self.session.query(db_models.Team)
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
        self.session.commit()
        self.log.info(f"User {db_user} was added to team {db_team} in db")

    def get_team(self, team_name: str) -> db_models.Team | None:
        """Getting team from db by name"""
        team = (
            self.session.query(db_models.Team)
            .filter(
                db_models.Team.name == team_name,
            )
            .first()
        )
        if not team:
            return None
        self.log.info(f"Team {team} was found in db")
        return team

    def get_b1_users_without_teams_online(self):
        users = self.session.query(db_models.User).filter(
            db_models.User.team == None,
            db_models.User.track == 1,
            db_models.User.type_of_presense == 'Онлайн'
            ).all()
        return users

    def get_b1_users_without_teams_offline(self):
        users = self.session.query(db_models.User).filter(
            db_models.User.team == None,
            db_models.User.track == 1,
            db_models.User.type_of_presense == 'Очно'
            ).all()
        return users

    def get_b2_users_without_teams(self):
        users = self.session.query(db_models.User).filter(
            db_models.User.team == None,
            db_models.User.track == 2
            ).all()
        return users

    def get_all_teams_with_members(self):
        # Execute the query to retrieve the team name and a list of team members

        result = self.session.query(
            db_models.Team.name,
            db_models.Team.id,
        ).all()

        # Format the results as a list of dictionaries
        team_info = [
            {'team_name': row.name, 'team_members': self._get_team_members(row.id)}
            for row in result
        ]

        return team_info

    def _get_team_members(self, team_id: int):
        members = self.session.query(db_models.User).filter(
            db_models.User.team == team_id
            ).all()
        return members

    def get_not_full_teams_b1(self):
        # Execute the query to retrieve the team name and a list of team members
        join_query = join(db_models.User, db_models.Team, db_models.User.team == db_models.Team.id)

        result = self.session.query(
            db_models.Team.name,
            func.array_agg(db_models.User.user_name).label('team_members')
        ).select_from(join_query).group_by(db_models.Team.name).all()

        # Format the results as a list of dictionaries
        team_info = [
            {'team_name': row.name, 'team_members': row.team_members}
            for row in result
            if len(row.team_members) < 3
        ]

        return team_info

    def get_users_without_tg_name(self):
        users = self.session.query(db_models.User).filter(
            db_models.User.telegram_name == None
            ).all()
        return users

    def get_all_teams_with_members_b1(self):
        # Execute the query to retrieve the team name and a list of team members

        result = self.session.query(
            db_models.Team.name,
            db_models.Team.id,
        ).all()

        # Format the results as a list of dictionaries
        team_info = [
            {'team_name': row.name, 'team_members': self._get_team_members(row.id)}
            for row in result
        ]
        team_info = [
            team
            for team in team_info
            if team['team_members'][0].track == 1
        ]

        return team_info


    # endregion

    # endregion
