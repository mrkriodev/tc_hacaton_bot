# Кнопки для диалоговых окон
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from dialogs.menu.states import BotMenu
from . import keyboards
from utils.text_message import welcome_text


def main_menu():
    return Window(
        Const(welcome_text),
        keyboards.main_menu(),
        state=BotMenu.select_main_menu,
    )
