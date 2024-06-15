from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from dialogs.menu.selected import (
    click_button_token_check_service,
)


def main_menu():
    return Group(
        Button(
            Const("Проверить смарт-контракт"),
            id="btn_list_token_service",
            on_click=click_button_token_check_service,
        ),
        width=1,
    )
