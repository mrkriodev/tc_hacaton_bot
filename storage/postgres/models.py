from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func,
    ForeignKey,
    UniqueConstraint,
    Float,
    Boolean,
    BigInteger,
    Text,
    JSON
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        res = ""
        for i, v in enumerate(cls.__name__):
            if i == 0:
                res += f"{v.lower()}"
                continue
            if v.isupper():
                res += f"_{v.lower()}"
                continue
            res += v
        return f"{res}"


class TcUser(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String, nullable=True)

    # tokens: Mapped[list["Token"]] = relationship(
    #     secondary="user_tokens",
    #     back_populates="users",
    # )
    # cross
    # tokens: Mapped[list["UserToken"]] = relationship(back_populates="user")


class TcSmartContract(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=True)
    analytic_info: Mapped[str] = mapped_column(String, nullable=True)
    transfer_analytic_info: Mapped[str] = mapped_column(String, nullable=True)
    # analyze_info_json: Mapped[JSON] = mapped_column(JSON, nullable=True)

    # contract_main_analytic: dict = {'creator': {'adr': None, 'balance': None, 'rate': None},
    #                                 'owner': {'adr': None, 'balance': None, 'rate': None},
    #                                 'is_renounced': None,
    #                                 'is_mintable': None,
    #                                 'is_burnable': None,
    #                                 'is_proxy': False,
    #                                 'is_self_destructable': None,
    #                                 'is_token_transferable': None,
    #                                 'transer_tax': None,
    #                                 'transfer_from_tax': None,
    #                                 }


class TcNotificationUser(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tc_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_notification: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="f"
    )


class TcMessageFromUser(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tc_user_id: Mapped[int] = mapped_column(ForeignKey("tc_user.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
