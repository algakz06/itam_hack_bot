from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject

from app.core.db import DBManager


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["db"] = self.db
        return await handler(event, data)
