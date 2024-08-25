import contextlib
from typing import AsyncIterator, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs)
from sqlalchemy.orm import DeclarativeBase

from app.db.config import settings

# We will inherit from the following base class to create each
# of the database models or classes (the ORM models)
class Base(DeclarativeBase):
    pass

# Load database secrets
# dbconfig = load_config()


# Create an async connection url from dbconfig
url_object = URL.create(
    "postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    database=settings.POSTGRES_DBNAME
)


class DatabaseSessionManger:
    def __init__(self, database_url: URL, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(database_url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False,
                                                bind=self._engine,
                                                expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManger is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    # connect is used with alembic for migrations
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManger is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    # This is the primary method of connecting to the DB
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

            
sessionmanager = DatabaseSessionManger(url_object,
                                       {"echo": settings.POSTGRES_ECHO,
                                        "pool_recycle": settings.POSTGRES_POOL_RECYCLE\
                                        })


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

        
