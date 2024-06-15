from typing import Tuple, Sequence

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from storage.postgres.dao.smartcontracts import TcSmartContractDAO
from storage.postgres.models import TcSmartContract


class TcSmartContractService:
    def __init__(self, session: AsyncSession):
        self.tc_sc_dao = TcSmartContractDAO(session=session)
        self.session = session

    async def update_sc_transfer_info(self, tc_smartcontract_id: int, updated_transfer_info: str):
        await self.tc_sc_dao.update_sc_transfer_info(tc_smartcontract_id, updated_transfer_info)
        await self.session.commit()

    async def get_sc_info(self, sc_id: int) -> Row[TcSmartContract]:
        result = await self.tc_sc_dao.get_sc_info(token_id=sc_id)
        return result
