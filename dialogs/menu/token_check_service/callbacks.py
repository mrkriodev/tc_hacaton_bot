import asyncio
from typing import Any, Coroutine

import aiohttp
from aiogram.fsm.state import State
from aiohttp import ClientTimeout

from config import settings
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode, BaseDialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from dialogs.menu.states import BotMenu
from dialogs.menu.token_check_service.states import TokenCheckMenu
from service.users import TCUsersService


async def click_one_provider(
    c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    ctx = manager.current_context()
    ctx.dialog_data.update({"provider_id": item_id})  # данные между стейтами
    ctx.dialog_data.update({"network_name": item_id})
    await manager.switch_to(TokenCheckMenu.input_sc_address_state)


async def input_token_address_callback(m: Message, widget: Any, manager: DialogManager):
    print(m.text)
    ctx = manager.current_context()
    ctx.dialog_data.update({"token_adr": m.text})
    # user_service: TCUsersService = manager.middleware_data.get("user_service")
    # await user_service.add_new_message_for_support(m.from_user.id, m.text)
    await m.answer("Запущена обработка смарт-контракта!")
    await manager.switch_to(TokenCheckMenu.sc_base_info_state, show_mode=ShowMode.DELETE_AND_SEND)


async def check_sc_source_code_callback(c: CallbackQuery,
                                        widget: Button,
                                        manager: DialogManager):
    ctx = manager.current_context()
    await c.answer("Запускаем анализ исходного кода...")
    analyzing_message = await c.message.answer("Анализируем исходный код...")
    manager.dialog_data.update({"source_code_not_analyzed": False})
    # await c.message.answer("Анализируем исходный код...")
    await manager.switch_to(TokenCheckMenu.sc_source_code_state, show_mode=ShowMode.DELETE_AND_SEND)
    # await asyncio.sleep(5)
    # await analyzing_message.delete()


async def check_sc_social_info_callback(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await c.answer("Запускаем анализ социальных характеристик...")
    analyzing_message = await c.message.answer("Запускаем анализ социальных характеристик...")
    manager.dialog_data.update({"social_info_not_analyzed": False})
    await manager.switch_to(TokenCheckMenu.sc_social_info_state, show_mode=ShowMode.DELETE_AND_SEND)


async def check_sc_ai_analyze_callback(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await c.answer("Запускаем анализ через AI-антифрод...")
    analyzing_message = await c.message.answer("Запускаем анализ через AI-антифрод...")
    manager.dialog_data.update({"ai_not_analyzed": False})
    await manager.switch_to(TokenCheckMenu.sc_ai_analyze_state, show_mode=ShowMode.DELETE_AND_SEND)


async def background_progress_updater(manager: BaseDialogManager,
                                      stop_event: asyncio.Event,
                                      switch_to_state: State):
    count = 1000
    for i in range(1, count + 1):
        if stop_event.is_set():
            print("Stopping progress updater as data has been fetched.")
            break
        await asyncio.sleep(1)
        await manager.update({
            "progress": (i % 10) * 100 / 10,
        })
    await asyncio.sleep(1)
    # await manager.done()  # "switch_to"
    # await manager.switch_to(state=TokenCheckMenu.sc_liquidity_state, show_mode=ShowMode.DELETE_AND_SEND)
    await manager.switch_to(state=switch_to_state, show_mode=ShowMode.DELETE_AND_SEND)


async def background_liquidity_url_fetch(sc_adr_in: str, provider_in: str,
                                         manager: BaseDialogManager,
                                         stop_event_in: asyncio.Event):
    _timeout = ClientTimeout(total=90)
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_LIQUIDITY_URL,
                                json={
                                    "sc_address": sc_adr_in,
                                    "symbol": "Undefined",
                                    "provider": provider_in}) as response:
            liquidity_analytic_result = await response.json()
            if liquidity_analytic_result is not None:
                for pool_name in ['uniswapv2', 'uniswapv3', 'pancakeswapv2', 'pancakeswapv3']:
                    if liquidity_analytic_result.get(pool_name, None) is not None:
                        if len(liquidity_analytic_result[pool_name]) == 0:
                            liquidity_analytic_result[pool_name] = None
            print(f"liquidity_analytic_result={liquidity_analytic_result}")
            await manager.update({'liquidity_info': liquidity_analytic_result})
            await manager.update(liquidity_analytic_result)
            await manager.update({'liquidity_not_analyzed': False})
            stop_event_in.set()


async def background_transfer_url_fetch(sc_adr_in: str, provider_in: str,
                                        manager: BaseDialogManager,
                                        stop_event_in: asyncio.Event):
    _timeout = ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_TRANSFER_URL,
                                json={
                                    "sc_address": sc_adr_in,
                                    "symbol": "Undefined",
                                    "provider": provider_in}) as response:
            transfer_analytic_result = await response.json()
            if response.status == 200:
                await manager.update(transfer_analytic_result)
            else:
                await manager.update({'transfer_info': None})
            await manager.update({'transfer_not_analyzed': False})
            stop_event_in.set()


async def check_sc_liquidity_callback(c: CallbackQuery,
                                      widget: Button,
                                      dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    dm_dd = dialog_manager.dialog_data
    await c.answer("Запускаем анализ ликвидности...")
    await c.message.answer("Запускаем анализ ликвидности...")

    stop_event = asyncio.Event()
    asyncio.create_task(background_progress_updater(dialog_manager.bg(),
                                                    stop_event,
                                                    TokenCheckMenu.sc_liquidity_state))
    asyncio.create_task(background_liquidity_url_fetch(sc_adr_in=dm_dd.get("token_adr"), provider_in=dm_dd.get("provider_id"),
                                                       manager=dialog_manager.bg(), stop_event_in=stop_event))
    # dm_dd.update({"liquidity_not_analyzed": False})
    # await manager.switch_to(TokenCheckMenu.sc_liquidity_state, show_mode=ShowMode.DELETE_AND_SEND)
    await dialog_manager.switch_to(TokenCheckMenu.progress_state, show_mode=ShowMode.DELETE_AND_SEND)


async def check_token_transfer_callback(c: CallbackQuery,
                                        widget: Button,
                                        dialog_manager: DialogManager):
    dm_dd = dialog_manager.dialog_data
    await c.answer("Запускаем анализ параметров передачи...")
    await c.message.answer("Запускаем анализ параметров передачи...")

    stop_transfer_fetcher_event = asyncio.Event()
    asyncio.create_task(background_progress_updater(dialog_manager.bg(),
                                                    stop_transfer_fetcher_event,
                                                    TokenCheckMenu.sc_transfer_info_state))
    asyncio.create_task(
        background_transfer_url_fetch(sc_adr_in=dm_dd.get("token_adr"), provider_in=dm_dd.get("provider_id"),
                                      manager=dialog_manager.bg(), stop_event_in=stop_transfer_fetcher_event))
    await dialog_manager.switch_to(TokenCheckMenu.progress_state, show_mode=ShowMode.DELETE_AND_SEND)
