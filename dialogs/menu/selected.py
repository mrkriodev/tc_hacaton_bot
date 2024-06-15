# Обработка нажатий на кнопки
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from .token_check_service.states import TokenCheckMenu

# main menu level 0


async def click_button_token_check_service(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer()
    await manager.start(TokenCheckMenu.select_list_providers)

