from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.utils.render_templates import render_template
from app.core import crud


router = Router()


@router.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext) -> None:
    """Cancel command handler."""
    await state.clear()
    await message.answer("Действие отменено")
