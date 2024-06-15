from typing import Tuple, Sequence

from sqlalchemy import update, select, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import join

from storage.postgres.models import TcSmartContract


class TcSmartContractDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_sc_transfer_info(self, tc_smartcontract_id: int, updated_transfer_info: str):
        stmt = (
            update(TcSmartContract)
            .where(TcSmartContract.id == tc_smartcontract_id)
            .values(transfer_analytic_info=updated_transfer_info)
        )
        await self.session.execute(stmt)

    async def get_sc_info(self, tc_sc_id: int) -> Row[TcSmartContract]:
        stmt = (
            select(TcSmartContract).where(TcSmartContract.id == tc_sc_id)
        )
        result = await self.session.execute(stmt)
        return result.one()


