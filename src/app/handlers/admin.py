from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

import random

from app.config import settings
from app.config import log
from app.models import db_models
from app.models.states import Broadcast
from app.utils.render_templates import render_template
from app.keyboards import reply_keyboards
from app.core.db import DBManager


router = Router()


@router.message(Command('shuffle_b1'), F.from_user.id == settings.TG_ADMIN_ID)
async def shuffle_teams(message: types.Message, db: DBManager):
    random_team_names = [
    "МИСИСовцы",
    "Кодеры МИСИСа",
    "Хакеры МИСИСа",
    "Инноваторы МИСИСа",
    "Алгоритмисты МИСИСа",
    "Команда МИСИСа",
    "Техногении МИСИСа",
    "Кибергении МИСИСа",
    "Квантовцы МИСИСа",
    "Программисты МИСИСа",
    "МИСИС-Кодеры",
    "Хакатон-МИСИС",
    "Команда-МИСИС",
    "Инновационный МИСИС",
    "Техно-гении МИСИС",
    "Кибер-МИСИС",
    "Алгоритмисты-МИСИС",
    "Программирование-МИСИС",
    "Разработчики-МИСИС",
    "Команда-Университета-МИСИС",
    "МИСИС-Геймеры",
    "Компьютерные-МИСИС",
    "Кодирование-МИСИС",
    "Технологии-МИСИС",
    "Инновационные-МИСИС",
    "Кибер-Команда-МИСИС",
    "Программные-МИСИС",
    "Разработка-МИСИС",
    "Техногенная-МИСИС",
    "Компьютерная-Команда-МИСИС",
    "МИСИС-Техники",
    "МИСИСики",
    "МИСИС и команда"
    ]

    users_online: list = db.get_b1_users_without_teams_online()
    users_offline: list = db.get_b1_users_without_teams_offline()
    random.shuffle(users_online)
    random.shuffle(users_offline)

    not_full_teams = db.get_not_full_teams_b1()

    for team in not_full_teams:
        member = users_offline.pop()
        db.add_user_to_team(member.telegram_id, team['team_name'])

    team_members = []
    for user in users_offline:
        if len(team_members) == 3:
            db.create_team(random_team_names[-1])
            team = db.get_team(random_team_names.pop())
            for member in team_members:
                db.add_user_to_team(member.telegram_id, team.name)
            team_members = []
        team_members.append(user)
    else:
        if team_members:
            if len(team_members) == 2:
                team_members.append(users_online.pop())
            db.create_team(random_team_names[-1])
            team = db.get_team(random_team_names.pop())
            for member in team_members:
                db.add_user_to_team(member.telegram_id, team.name)
            team_members = []

    for user in users_online:
        if len(team_members) == 3:
            db.create_team(random_team_names[-1])
            team = db.get_team(random_team_names.pop())
            for member in team_members:
                db.add_user_to_team(member.telegram_id, team.name)
            team_members = []
        team_members.append(user)
    else:
        if team_members:
            db.create_team(random_team_names[-1])
            team = db.get_team(random_team_names.pop())
            for member in team_members:
                db.add_user_to_team(member.telegram_id, team.name)
            team_members = []

    await message.answer('Команды перемешаны')


@router.message(Command('b2_without_team'), F.from_user.id == settings.TG_ADMIN_ID)
async def get_b2_members_without_team(message: types.Message, db: DBManager):
    users: list[db_models.User] = db.get_b2_users_without_teams()
    reply_message: str = ''
    for user in users:
        reply_message += f'{user.user_name}, {user.university_group}, {user.specialty}, {user.telegram_name}\n\n'
    await message.answer(reply_message)


@router.message(Command('get_teams'), F.from_user.id == settings.TG_ADMIN_ID)
async def get_teams(message: types.Message, db: DBManager):
    teams = db.get_all_teams_with_members()
    for team in teams:
        reply_message = render_template('team_list.j2', {
            'teamname': team['team_name'],
            'team_members': team['team_members'],
        })
        await message.answer(reply_message)