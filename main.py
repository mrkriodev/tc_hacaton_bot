import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiohttp import web

from routers import router
from bot import bot, dp
from config import settings, bot_command
from dialogs import include_dialogs
from dialogs.error import on_unknown_intent, on_unknown_state
from middleware.setup import register_global_middleware


def register_functions():
    register_global_middleware(dp)
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )

    include_dialogs(dp)
    setup_dialogs(dp)

    dp.include_router(router)

    json_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
    logging.basicConfig(level=logging.INFO, format=json_format)


async def register_commands():
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=bot_command, scope=BotCommandScopeAllPrivateChats()
    )


async def run_polling():
    await register_commands()
    await dp.start_polling(bot, skip_updates=True)


async def on_startup(bot: Bot) -> None:
    await register_commands()
    logging.info("Registration webhook")
    await bot.set_webhook(
        f"{settings.WEBHOOK_SETTINGS.BASE_WEBHOOK_URL}{settings.WEBHOOK_SETTINGS.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SETTINGS.WEBHOOK_SECRET,
    )


def run_webhook():
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SETTINGS.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path="/")
    setup_application(app, dp, bot=bot)
    web.run_app(
        app,
        host=settings.WEBHOOK_SETTINGS.WEB_SERVER_HOST,
        port=settings.WEBHOOK_SETTINGS.WEB_SERVER_PORT,
    )


if __name__ == "__main__":
    register_functions()
    if settings.START_POOLING is True:
        asyncio.run(run_polling())
    else:
        run_webhook()
