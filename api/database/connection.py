from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import get_setting


setting = get_setting()


async_engine = create_async_engine(
    url=setting.database_url,
    pool_size=50,
    max_overflow=50,
    pool_recycle=1800,
    pool_timeout=3,
    pool_pre_ping=True
)


async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)
Base = declarative_base()