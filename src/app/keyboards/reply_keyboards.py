from aiogram import types


def get_start_keyboard() -> types.ReplyKeyboardMarkup:
    markup = [
        [
            types.KeyboardButton(text="Б1"),
        ],
        [
            types.KeyboardButton(text="Б2"),
        ],
    ]
    return types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)

def get_team_keyboard() -> types.ReplyKeyboardMarkup:
    markup = [
        [
            types.KeyboardButton(text="Есть команда"),
        ],
        [
            types.KeyboardButton(text="Нет команды"),
        ],
    ]
    return types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)


def get_specialty_keyboard() -> types.ReplyKeyboardMarkup:
    markup = [
        [
            types.KeyboardButton(text="Frontend"),
            types.KeyboardButton(text="Backend"),
        ],
        [
            types.KeyboardButton(text="Fullstack"),
            types.KeyboardButton(text="Дизайнер"),
        ],
        [
            types.KeyboardButton(text="ML/DS/AI"),
            types.KeyboardButton(text="Не знаю"),
        ]
    ]
    return types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)


def get_presense_keyboard() -> types.ReplyKeyboardMarkup:
    markup = [
        [
            types.KeyboardButton(text="Очно"),
            types.KeyboardButton(text="Онлайн"),
        ],
    ]
    return types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)