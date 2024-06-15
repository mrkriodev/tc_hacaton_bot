import operator

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group, Button
from aiogram_dialog.widgets.common import WhenCondition, Whenable
from aiogram_dialog.widgets.text import Format, Const
from typing import Dict


def choose_availavle_providers(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_scroll_list_providers",
            # item_id_getter=operator.itemgetter(1),
            item_id_getter=operator.itemgetter(0),
            items="data",
            on_click=on_click,
        ),
        id="list_token_service_ids",
        width=3,
        height=3,
        hide_on_single_page=True,
    )


def kbn_processed_input_token_adr(on_click):
    return MessageInput(
        func=on_click,
        content_types=["text"],
    )


def is_can_analyze_source_code(data: Dict, widget: Whenable, manager: DialogManager):
    if data['is_proxy']['value']:
        return False
    else:
        return data.get("source_code_not_analyzed")


def is_can_study_transfer(data: Dict, widget: Whenable, manager: DialogManager):
    if str(data["provider_id"]).lower() not in ["eth", "bsc", "sibr"]:
        return False
    else:
        return data.get("transfer_not_analyzed")


def is_can_analyze_liquidity(data: Dict, widget: Whenable, manager: DialogManager):
    if str(data["provider_id"]).lower() not in ["eth", "bsc"]:
        return False
    else:
        return data.get("liquidity_not_analyzed")


def kbn_analyze_sc_deeper(on_click_deep_transfer_study,
                          on_click_source_code_study,
                          on_click_liquidity_study,
                          on_click_social_info,
                          on_click_ai_analyze):
    return Group(
        Button(
            Const("Точнее исследовать передачу токенов"),
            id="check_contract_deeper_id",
            on_click=on_click_deep_transfer_study,
            # when="transfer_not_analyzed"
            when=is_can_study_transfer
        ),
        Button(
            Const("Социальная вовлеченность контракта"),
            id="check_contract_socaial_info_id",
            on_click=on_click_social_info,
            when="social_info_not_analyzed"
        ),
        Button(
            Const("Исследовать исходный код смарт-контракта"),
            id="check_contract_source_code_id",
            on_click=on_click_source_code_study,
            #when="source_code_not_analyzed"
            when=is_can_analyze_source_code
        ),
        Button(
            Const("Исследовать ликвидность токена смарт-контракта"),
            id="check_liquidity_id",
            on_click=on_click_liquidity_study,
            # when="liquidity_not_analyzed"
            when=is_can_analyze_liquidity
        ),
        Button(
            Const("Исследовать контракт через AI-антифрод"),
            id="check_ai_analyze_id",
            on_click=on_click_ai_analyze,
            when="ai_not_analyzed"
        ),
        when="has_base_analyse"
    )


def get_list_percent(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_list_percent",
            item_id_getter=operator.itemgetter(1),
            items="data",
            on_click=on_click,
        ),
        width=4,
        height=2,
        id="scroll_list_percent",
        hide_on_single_page=True,
    )
