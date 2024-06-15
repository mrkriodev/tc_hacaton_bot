import base64
from io import BytesIO

from aiogram.types import InputFile, BufferedInputFile
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Back
from aiogram_dialog.widgets.text import Const, Format, Multi, Progress

from dialogs.menu.gatters import get_percent_for_token
from dialogs.menu.token_check_service.states import TokenCheckMenu

from utils.text_message import (
    const_text_list_service_token,
    wrap_deeper_info_about_sc, CustomJinjaForBaseInfo, CustomSourceCodeAnalyticJinja, CustomFullInfoJinja,
    CustomLiquidityJinja, CustomJinjaForTransferInfo, CustomJinjaForSocialInfo, CustomJinjaForAiAnalyze,
)
from . import keyboards
from . import callbacks
from . import gatters
from .gatters import get_bg_data


def token_check_service_uppermost():
    window = Window(
        Const(const_text_list_service_token),
        keyboards.choose_availavle_providers(
            callbacks.click_one_provider  # callback на каждый button
        ),
        # Cancel(Const("Назад")),
        state=TokenCheckMenu.select_list_providers,
        getter=gatters.get_available_providers,
    )
    return window


def input_token_address_window():
    window = Window(
        Const("Введите адрес СК"),
        keyboards.kbn_processed_input_token_adr(callbacks.input_token_address_callback),
        Back(Const("Назад")),
        state=TokenCheckMenu.input_sc_address_state,
    )
    return window


def sc_base_info_window():
    window = Window(
        CustomJinjaForBaseInfo(),
        keyboards.kbn_analyze_sc_deeper(callbacks.check_token_transfer_callback,
                                        callbacks.check_sc_source_code_callback,
                                        callbacks.check_sc_liquidity_callback,
                                        callbacks.check_sc_social_info_callback,
                                        callbacks.check_sc_ai_analyze_callback),
        Back(Const("Назад")),
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_base_info_state,
        getter=gatters.get_base_info_about_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


async def custom_render(dialog_manager: DialogManager, **kwargs):
    data = await dialog_manager.dialog_data.get('social_info', None)
    custom_jinja = CustomJinjaForSocialInfo()
    text = await custom_jinja.render(data)

    # Если есть base64 изображение, отправляем его отдельно
    if data.get('base64_image'):
        # await send_base64_image(dialog_manager, data['base64_image'], caption=text)
        text = ""  # Очищаем текст, чтобы не отправлять его дважды

    return text


def sc_social_info_window():
    window = Window(
        CustomJinjaForSocialInfo(),
        Back(Const("Показать текущий отчет")),  # Вот тут Назад так работает
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_social_info_state,
        getter=gatters.get_social_info_about_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def sc_ai_analyze_window():
    window = Window(
        CustomJinjaForAiAnalyze(),
        Back(Const("Показать текущий отчет")),  # Вот тут Назад так работает
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_ai_analyze_state,
        getter=gatters.get_ai_analyze_info,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def sc_source_code_analytic_window():
    window = Window(
        CustomSourceCodeAnalyticJinja(),
        Back(Const("Показать текущий отчет")),  # Вот тут Назад так работает
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_source_code_state,
        getter=gatters.get_analytic_source_code_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def sc_liquidity_analytic_window():
    window = Window(
        CustomLiquidityJinja(),
        # Const("Еуые"),
        Back(Const("Показать текущий отчет")),  # Вот тут Назад так работает
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_liquidity_state,
        getter=gatters.get_analytic_liquidity_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def token_transfer_info_window():
    window = Window(
        CustomJinjaForTransferInfo(),
        Back(Const("Показать текущий отчет")),  # Вот тут Назад так работает
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_transfer_info_state,
        getter=gatters.get_transfer_info_about_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def sc_full_info_window_one():
    window = Window(
        # wrap_for_base_sc_info,
        CustomFullInfoJinja(),
        keyboards.kbn_analyze_sc_deeper(callbacks.check_token_transfer_callback,
                                        callbacks.check_sc_source_code_callback,
                                        callbacks.check_sc_liquidity_callback,
                                        callbacks.check_sc_social_info_callback,
                                        callbacks.check_sc_ai_analyze_callback),
        Cancel(Const("Завершить обработку")),
        state=TokenCheckMenu.sc_full_info_state_one,
        getter=gatters.get_full_info_about_sc,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return window


def sc_full_info_window_two():
    window = sc_full_info_window_one()
    window.state = TokenCheckMenu.sc_full_info_state_two
    return window


def sc_full_info_window_three():
    window = sc_full_info_window_one()
    window.state = TokenCheckMenu.sc_full_info_state_three
    return window


def sc_full_info_window_four():
    window = sc_full_info_window_one()
    window.state = TokenCheckMenu.sc_full_info_state_four
    return window


def sc_full_info_window_five():
    window = sc_full_info_window_one()
    window.state = TokenCheckMenu.sc_full_info_state_five
    return window


def progress_dialog():
    window = Window(
         Multi(
             Const("Ваш запрос обрабатывается, пожалуйста подождите..."),
             Progress("progress", 10),
         ),
         state=TokenCheckMenu.progress_state,
         getter=get_bg_data,
    )
    return window
