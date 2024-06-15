from aiogram.fsm.state import StatesGroup, State


class TokenCheckMenu(StatesGroup):
    select_list_providers = State()
    input_sc_address_state = State()
    sc_base_info_state = State()  # in state of window
    sc_full_info_state_one = State()
    sc_source_code_state = State()
    sc_full_info_state_two = State()
    sc_transfer_info_state = State()
    sc_full_info_state_three = State()
    sc_full_info_state_four = State()
    sc_full_info_state_five = State()
    sc_liquidity_state = State()
    sc_social_info_state = State()
    sc_ai_analyze_state = State()
    progress_state = State()
