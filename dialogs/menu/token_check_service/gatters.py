import aiohttp
from aiogram_dialog import DialogManager
# from service.tokens import TokenService
from aiohttp import ClientTimeout

from config import settings
from service.users import TCUsersService


async def get_available_providers(**middleware_data):
    return {'data': [("SIBR", "4"), ("ETH", "1"), ("BSC", "2")]}  #, ("TRX", "3")]}


async def get_list_token_service(**middleware_data):
    user_service: TCUsersService = middleware_data.get("user_service")
    list_token = await user_service.get_list_token(is_tuple=True)
    return {"data": list_token}


async def get_base_info_about_sc(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.dialog_data
    # запустить обработчики
    _timeout = ClientTimeout(total=90)
    analyze_result = None
    ctx.update({'has_base_analyse': False})
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_BASE_URL,
                                json={
                                    "sc_address": ctx.get("token_adr"),
                                    "symbol": "undefined",
                                    "provider": ctx.get("provider_id")}) as response:
            analyze_result = await response.json()
            if response.status == 200:
                ctx.update({'has_base_analyse': True})
            else:
                ctx.update({'error_msg': analyze_result.get('detail', "произошла ошибка на сервере")})

    if not ctx.get('has_base_analyse'):
        return ctx
    if analyze_result.get('has_source_code', False):
        ctx.update({'source_code_not_analyzed': True})
    else:
        ctx.update({'source_code_not_analyzed': False})
    if analyze_result.get('token_id', False):
        ctx.update({'social_info_not_analyzed': True})
    else:
        ctx.update({'social_info_not_analyzed': False})
    ctx.update({'liquidity_not_analyzed': True})
    ctx.update({'transfer_not_analyzed': True})
    ctx.update({'ai_not_analyzed': True})
    ctx.update(analyze_result)
    return ctx


async def get_social_info_about_sc(dialog_manager: DialogManager, **middleware_data):
    dm_dd = dialog_manager.dialog_data
    # запустить обработчики
    _timeout = ClientTimeout(total=30)
    sc_token_id = dm_dd.get('token_id', 'undefined')
    soc_info_result = None
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SOCIAL_INFO_URL,
                                json={
                                    "sc_address": dm_dd.get("token_adr"),
                                    "symbol": sc_token_id,
                                    "provider": dm_dd.get("provider_id")}) as response:
            soc_info_result = await response.json()
            if response.status == 200:
                dm_dd.update({'social_info': soc_info_result})
            else:
                dm_dd.update({'error_msg': soc_info_result.get('detail', "произошла ошибка на сервере")})
    if dm_dd.get('social_info', None) is None:
        return dm_dd
    print(f"soc_info_result={soc_info_result}")
    dm_dd.update({'social_info_not_analyzed': False})
    return {'social_info': soc_info_result}


async def get_ai_analyze_info(dialog_manager: DialogManager, **middleware_data):
    dm_dd = dialog_manager.dialog_data
    _timeout = ClientTimeout(total=90)
    ai_analyze_result = None
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_AI_URL,
                                json={
                                    "sc_address": dm_dd.get("token_adr"),
                                    "symbol": "undefined",
                                    "provider": dm_dd.get("provider_id")}) as response:
            ai_analyze_result = await response.json()
            if response.status == 200:
                dm_dd.update(ai_analyze_result)
            else:
                dm_dd.update({'error_msg': ai_analyze_result.get('detail', "произошла ошибка на сервере")})
    if dm_dd.get('ai_analyze_result', None) is None:
        return dm_dd
    print(f"ai_analyze_result={ai_analyze_result}")
    dm_dd.update({'ai_not_analyzed': False})
    return ai_analyze_result



async def get_bg_data(dialog_manager: DialogManager, **kwargs):
    return {
        "progress": dialog_manager.dialog_data.get("progress", 0)
    }


async def get_full_info_about_sc(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.dialog_data
    return ctx


async def get_analytic_source_code_sc(dialog_manager: DialogManager, **middleware_data):
    dm_dd = dialog_manager.dialog_data
    # запустить обработчики
    _timeout = ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_SOURCE_CODE_URL,
                                json={
                                    "sc_address": dm_dd.get("token_adr"),
                                    "symbol": "undefined",
                                    "provider": dm_dd.get("provider_id")}) as response:
            source_code_analytic_result = await response.json()
    dm_dd.update(source_code_analytic_result)
    dm_dd.update({'source_code_not_analyzed': False})
    return source_code_analytic_result


async def get_analytic_liquidity_sc(dialog_manager: DialogManager, **middleware_data):
    dm_dd = dialog_manager.dialog_data
    liquidity_info = dm_dd.get("liquidity_info")
    if liquidity_info is not None:
        return liquidity_info
    # запустить обработчики
    _timeout = ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_LIQUIDITY_URL,
                                json={
                                    "sc_address": dm_dd.get("token_adr"),
                                    "symbol": "undefined",
                                    "provider": dm_dd.get("provider_id")}) as response:
            liquidity_analytic_result = await response.json()
    dm_dd.update({'liquidity_info': liquidity_analytic_result})
    dm_dd.update(liquidity_analytic_result)
    dm_dd.update({'liquidity_not_analyzed': False})
    return liquidity_analytic_result


async def get_transfer_info_about_sc(dialog_manager: DialogManager, **middleware_data):
    dm_dd = dialog_manager.dialog_data
    transfer_info = dm_dd.get("transfer_info")
    if transfer_info is not None:
        return {'transfer_info': transfer_info}
    # запустить обработчики
    _timeout = ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=_timeout) as session:
        async with session.post(settings.ANALYZE_SERVICE_TRANSFER_URL,
                                json={
                                    "sc_address": dm_dd.get("token_adr"),
                                    "symbol": "undefined",
                                    "provider": dm_dd.get("provider_id")}) as response:
            transfer_analytic_result = await response.json()
    # dm_dd.update({'transfer_info': transfer_analytic_result})
    dm_dd.update(transfer_analytic_result)
    dm_dd.update({'transfer_not_analyzed': False})
    return transfer_analytic_result
    # #session = middleware_data.get("session_db")
    # #token_service: TcSmartContractService = TcSmartContractService(session)
    # ctx = dialog_manager.dialog_data
    # # list_info_token = await token_service.get_information_token(
    # #     int(ctx.get("sc_id"))
    # # )
    # sc_adr = ctx.get("token_adr")
    # return {"token_name": sc_adr, "network_name": ctx.get("provider_id")}
