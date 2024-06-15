from aiogram_dialog import Dialog

import dialogs.menu.token_check_service.windows as token_check_service_windows
from . import windows


def bot_menu_dialogs():
    return [
        Dialog(
            windows.main_menu(),
        ),
        Dialog(
            token_check_service_windows.token_check_service_uppermost(),
            token_check_service_windows.input_token_address_window(),
            token_check_service_windows.sc_base_info_window(),
            token_check_service_windows.sc_full_info_window_one(),
            token_check_service_windows.sc_source_code_analytic_window(),
            token_check_service_windows.sc_full_info_window_two(),
            token_check_service_windows.sc_liquidity_analytic_window(),
            token_check_service_windows.sc_full_info_window_three(),
            token_check_service_windows.sc_social_info_window(),
            token_check_service_windows.sc_full_info_window_four(),
            token_check_service_windows.token_transfer_info_window(),
            token_check_service_windows.sc_full_info_window_five(),
            token_check_service_windows.sc_ai_analyze_window(),
            token_check_service_windows.progress_dialog(),
        ),
    ]
