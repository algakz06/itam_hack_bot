from aiogram.fsm.state import StatesGroup, State


class Registarion(StatesGroup):
    track = State()
    team = State()
    name = State()
    group = State()
