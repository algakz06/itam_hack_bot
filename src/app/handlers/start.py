from aiogram import types, Router
from aiogram.filters import CommandStart
from sqlalchemy.orm import Session

from app.utils.render_templates import render_template
from app.core import crud


router = Router()


@router.message(CommandStart())
async def start(message: types.Message, session: Session):
    user = crud.get_user(session, message.from_user.id)
    if user:
        await message.answer("Вы уже зарегистрированы")
        return

    answer = render_template("start.j2")
    await message.answer(answer)
    crud.add_user_to_db(session, message.from_user.id)
