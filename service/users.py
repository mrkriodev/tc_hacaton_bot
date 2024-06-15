from typing import Tuple

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from storage.postgres.dao.users import TCUserDAO
from storage.postgres.dto import TCUserDTO, TCMessageSupportDTO


class TCUsersService:
    def __init__(self, session: AsyncSession):
        self.users_dao = TCUserDAO(session=session)
        self.session = session

    @staticmethod
    def convert_message_to_dto(message: Message):
        return TCUserDTO(
            id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
        )

    async def add_new_user(self, tcuser: TCUserDTO) -> True:
        find_user = await self.users_dao.get_user_by_id(tcuser_id=tcuser.id)
        if not find_user:
            await self.users_dao.create_user(tcuser)
        await self.session.commit()
        return True

    async def add_new_message_for_support(self, user_id: int, message: str):
        await self.users_dao.add_new_message_for_support(
            TCMessageSupportDTO(tcuser_id=user_id, message=message)
        )
        await self.session.commit()
