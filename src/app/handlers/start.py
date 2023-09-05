from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from app.core.db import DBManager
from app.models.states import Registarion, TeamBuild, NoTeam
from app.utils.render_templates import render_template
from app.keyboards import reply_keyboards


router = Router()


@router.message(CommandStart())
async def start(message: types.Message, db: DBManager, state: FSMContext) -> None:
    user = db.get_user(message.from_user.id)

    if user:
        await message.answer("Вы уже зарегистрированы")
        return

    answer = render_template("start.j2")

    keyboard = reply_keyboards.get_start_keyboard()
    await message.answer(answer, reply_markup=keyboard)

    await state.set_state(Registarion.track)


@router.message(Registarion.track)
async def get_track(message: types.Message, state: FSMContext) -> None:
    if message.text == 'Б1':
        await state.set_data({"track": 1})
    elif message.text == 'Б2':
        await state.set_data({"track": 2})
    await message.answer("Есть ли у тебя команда?", reply_markup=reply_keyboards.get_team_keyboard())

    await state.set_state(Registarion.team)


@router.message(Registarion.team)
async def get_team(message: types.Message, state: FSMContext) -> None:
    if message.text == "Есть команда":
        await message.answer("Отлично! Введи название команды")
        await state.set_state(TeamBuild.team_name)
    elif message.text == "Нет команды":
        await message.answer("Ничего страшного, мы разберемся")
        await message.answer("Напиши свое ФИО", reply_markup=None)
        await state.set_state(NoTeam.name)


@router.message(TeamBuild.team_name)
async def get_team_name(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    data['team_name'] = message.text
    await state.set_data(data)
    await message.answer("Теперь поочереди в одном сообщении введи ФИО членов команды, каждый в одном сообщении, как только закончил введи команду /stop")
    await state.set_state(TeamBuild.team_member)


@router.message(TeamBuild.team_member, Command('stop'))
async def stop_accepting_team_members(message: types.Message, state: FSMContext, db: DBManager):
    data = await state.get_data()
    team_name = data.get('team_name', '')
    team = data.get('team')
    if len(team) < 2:
        await message.answer('Кажется ты где-то ошибся, введи /cancel и начни заново')
        return

    db.create_team(
        team_name=team_name,
    )

    team_in_db = db.get_team(team_name)

    for member in team:
        db.create_user(
            tg_user_id=message.from_user.id,
            telegram_name=message.from_user.username,
            team=team_in_db.id,
            track=data['track'],
            user_name=member,
            )

    await message.answer('Спасибо за регистрацию')
    await state.clear()

@router.message(TeamBuild.team_member)
async def get_team_member(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    team = data.get('team', [])
    if (len(team) < 3 and data['track'] == 1) or (len(team) < 5 and data['track'] == 2):
        team.append(message.text)
        data['team'] = team
        await state.set_data(data)
        await message.answer(f'Записал давай дальше, если закончил введи /stop, в команде человек {len(team)} из {3 if data["track"] == 1 else 5}')
    else:
        await message.answer('Перебор команды, введи /cancel, придется начать заново, введи /start')
        await state.clear()

@router.message(NoTeam.name)
async def get_member_name(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    data['name'] = message.text
    await state.set_data(data)
    await message.answer('Введи свою академическую группу')
    await state.set_state(NoTeam.group)


@router.message(NoTeam.group)
async def get_member_group(message: types.Message, db: DBManager, state: FSMContext) -> None:
    data = await state.get_data()
    data['group'] = message.text
    await state.set_data(data)

    data = await state.get_data()

    if data['track'] == 1:
        await message.answer('Спасибо за регистрацию')
        db.create_user(
            tg_user_id=message.from_user.id,
            telegram_name=message.from_user.username,
            track=data['track'],
            user_name=data['name'],
            university_group=data['group'],
            )
        await state.clear()
    else:
        await message.answer(
            'Выбери свою специальность, например Frontend разработчик',
            reply_markup=reply_keyboards.get_specialty_keyboard()
            )
        await state.set_state(NoTeam.specialty)


@router.message(NoTeam.specialty)
async def get_member_specialty(message: types.Message, db: DBManager, state: FSMContext) -> None:
    data = await state.get_data()
    db.create_user(
        tg_user_id=message.from_user.id,
        telegram_name=message.from_user.username,
        track=data['track'],
        user_name=data['name'],
        university_group=data['group'],
        specialty=message.text,
        )
    await message.answer('Спасибо за регистрацию', reply_markup=None)
    await state.clear()