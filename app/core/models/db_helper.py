from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from core.config import settings
class DbHelper:
    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
    
    async def dispose(self)->None:
        await self.engine.dispose()

    async def session_getter(self)->AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DbHelper(db_url=str(settings.db_config.url),
                    echo=settings.db_config.echo,
                    echo_pool=settings.db_config.echo_pool,
                    pool_size=settings.db_config.pool_size,
                    max_overflow=settings.db_config.max_overflow
                    )
