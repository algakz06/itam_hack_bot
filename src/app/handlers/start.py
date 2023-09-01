from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from app import keyboards

from app.models.states import Registarion, TeamBuild, NoTeam
from app.utils.render_templates import render_template
from app.keyboards import reply_keyboards
from app.core import crud


router = Router()


@router.message(CommandStart())
async def start(message: types.Message, session: Session, state: FSMContext) -> None:
    user = crud.get_user(session, message.from_user.id)

    if user:
        await message.answer("Вы уже зарегистрированы")
        return

    answer = render_template("start.j2")

    keyboard = reply_keyboards.get_start_keyboard()
    await message.answer(answer, reply_markup=keyboard)

    crud.add_user_to_db(session, message.from_user.id)

    await state.set_state(Registarion.track)


@router.message(Registarion.track)
async def get_track(message: types.Message, state: FSMContext) -> None:
    if message.text == 'Б1':
        await state.set_data({"track": 1})
    elif message.text == 'Б2':
        await state.set_data({"track": 2})
    await message.answer("Есть ли у тебя команда?", reply_markup=reply_keyboards.get_team_keyboard())

    await Registarion.next()


@router.message(Registarion.team)
async def get_team(message: types.Message, state: FSMContext) -> None:
    if message.text == "Есть команда":
        await message.answer("Отлично! Введи название команды")
        await state.set_data(TeamBuild.team_name)
    elif message.text == "Нет команды":
        await message.answer("Ничего страшного, мы разберемся")
        await message.answer("Напиши свое ФИО")
        await state.set_state(NoTeam.name)


@router.message(TeamBuild.team_name)
async def get_team_name(message: types.Message, state: FSMContext) -> None:
    await state.set_data({'team_name': message.text})
    await message.answer("Теперь поочереди в одном сообщении введи ФИО членов команды, каждый в одном сообщении")
    await state.set_state(TeamBuild.team_member)


@router.message(TeamBuild.team_member)
async def get_team_member(message: types.Message, state: FSMContext) -> None:
    ...


@router.message(NoTeam.name)
async def get_member_name(message: types.Message, state: FSMContext) -> None:
    ...
    await state.set_state(NoTeam.group)


@router.message(NoTeam.group)
async def get_member_group(message: types.Message, state: FSMContext) -> None:
    ...