import asyncio

from aiogram import Bot

from config import settings


def get_adjust(mass_kb, chunk_size: int = 2):
    return [
        len(mass_kb[i : i + chunk_size]) for i in range(0, len(mass_kb), chunk_size)
    ]


async def send_message(bot: Bot, chat_id, message):
    bot = await bot.send_message(
        chat_id=chat_id,
        text=message,
    )
    await bot.bot.session.close()
    return bot


async def send_message_bot(chat_id: int, text: str):
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
    await bot.session.close()


async def async_send_messages(tasks: list):
    # count 30 users
    await asyncio.gather(*tasks)
