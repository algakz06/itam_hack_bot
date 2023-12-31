from aiogram.fsm.state import StatesGroup, State


class Registarion(StatesGroup):
    type_of_presense = State()
    track = State()
    team = State()


class NoTeam(StatesGroup):
    name = State()
    group = State()
    specialty = State()


class TeamBuild(StatesGroup):
    team_name = State()
    team_member = State()


class Broadcast(StatesGroup):
    track = State()
    message = State()