from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from dialogs.menu.states import BotMenu

router = Router(name=__name__)


@router.message(Command("menu"))
async def menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotMenu.select_main_menu, mode=StartMode.RESET_STACK)
