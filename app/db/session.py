from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from app.core.config import ogas_stuff_db_settings

engine = create_async_engine(url=ogas_stuff_db_settings.url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)
