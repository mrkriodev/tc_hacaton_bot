from typing import List, Tuple, Any, Sequence

from sqlalchemy import select, insert, update, delete, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, join

from storage.postgres.models import (
    TcUser,
    TcSmartContract,
    TcMessageFromUser,
)
from storage.postgres.dto import TCUserDTO, TCMessageSupportDTO


class TCUserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: TCUserDTO) -> None:
        user = TcUser(**(user.model_dump()))
        self.session.add(user)

    async def get_user_by_id(self, tcuser_id: int) -> TcUser | None:
        query = select(TcUser).where(TcUser.id == tcuser_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add_new_message_for_support(self, message: TCMessageSupportDTO):
        msg = TcMessageFromUser(**(message.model_dump()))
        self.session.add(msg)
