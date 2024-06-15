from pydantic import BaseModel


class TCUserDTO(BaseModel):
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str | None


class TCMessageSupportDTO(BaseModel):
    tcuser_id: int
    message: str


class TCSmartContractDTO(BaseModel):
    id: int
    provider: str
    symbol: str
    analyztic_info: str
    transfer_analytic_info: str
