from aiogram.fsm.state import StatesGroup, State


class Registarion(StatesGroup):
    track = State()
    team = State()


class NoTeam(StatesGroup):
    name = State()
    group = State()


class TeamBuild(StatesGroup):
    team_name = State()
    team_member = State()


class Broadcast(StatesGroup):
    track = State()
    message = State()