from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(
    settings.POSTGRES_DSN.unicode_string(),
    echo=True if settings.DEBUG_MODE_POSTGRES else False,
)
async_session_marker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_marker() as session:
        yield session
