from aiogram import Dispatcher

from middleware.database_session import DataBaseSessionMiddleware
from middleware.init_services import InitServiceMiddleware
from storage.postgres.driver import async_session_marker


def register_global_middleware(dp: Dispatcher):
    dp.update.outer_middleware(DataBaseSessionMiddleware(async_session_marker))
    dp.update.middleware(InitServiceMiddleware())
