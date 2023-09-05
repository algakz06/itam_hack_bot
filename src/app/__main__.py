# region third-party imports
from aiogram import Bot, Dispatcher

import asyncio
from sqlalchemy.orm import sessionmaker

# endregion

# region local imports
from app.config import settings
from app.config import log
from app.middlewares.db_middleware import DbSessionMiddleware
from app.core.db import DBManager

# region routers
from app.handlers.start import router as start_router
from app.handlers.admin import router as admin_router
from app.handlers.cancel import router as cancel_router

# endregion


# endregion
def setup_handlers(dp: Dispatcher):
    """
    Setup all handlers
    """
    dp.include_router(cancel_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)


def setup_middlewares(db: DBManager):
    """
    Setup middlewares
    """
    start_router.message.middleware(DbSessionMiddleware(db))
    admin_router.message.middleware(DbSessionMiddleware(db))


async def main():
    """Initialize bot and dispatcher"""
    bot = Bot(token=settings.TG_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    """Initialize database"""
    db = DBManager(log)

    """Setup middlewares"""
    setup_middlewares(db)

    """Setup handlers"""
    setup_handlers(dp)

    """Start polling"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
