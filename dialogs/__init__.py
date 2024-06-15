from aiogram import Dispatcher
from aiogram_dialog.setup import DialogRegistry
from aiohttp import web

from . import menu


def include_dialogs(dp: Dispatcher):
    for dialog in [
        *menu.bot_menu_dialogs(),
    ]:
        dp.include_router(dialog)  # register a dialog
