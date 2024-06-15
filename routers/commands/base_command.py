from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command, CommandStart
from service.users import TCUsersService
from utils.text_message import text_command_start

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):  # , user_service: TCUsersService):
    # await user_service.add_new_user(
    #     user=user_service.convert_message_to_dto(message),
    # )
    await message.answer(text_command_start)


@router.message(Command("help", prefix="!/"))
async def help(message: Message):
    await message.answer(
        "1. Чтобы задать вопрос необходимо ввести команду /menu\n"
        "2. Выбрать пункт меню *Техническая поддержка*\n"
        "3. Ввести интересующий вопрос"
    )
