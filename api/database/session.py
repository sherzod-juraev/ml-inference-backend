from sqlalchemy.ext.asyncio import AsyncSession
from .connection import async_session


async def get_db() -> AsyncSession:

    async with async_session() as db:
        try:
            yield db
        except Exception as exc:
            await db.rollback()
            raise exc
        finally:
            await db.close()