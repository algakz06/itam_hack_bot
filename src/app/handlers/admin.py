from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from app import keyboards

from app.models.states import Broadcast
from app.utils.render_templates import render_template
from app.keyboards import reply_keyboards
from app.core.db import DBManager


router = Router()


@router.message(Command('shuffle'))
async def shuffle_teams(message: types.Message, db: DBManager, state: FSMContext):
    ...


@router.message(Command('broadcast'))
async def broadcast(message: types.Message, state: FSMContext):
    ...
    await state.set_state(Broadcast.track)


@router.message(Broadcast.track)
async def get_track(message: types.Message, state: FSMContext):
    ...
    await state.set_state(Broadcast.message)

@router.message(Broadcast.message)
async def get_message_for_broadcast(message: types.Message, db: DBManager, state: FSMContext):
    ...