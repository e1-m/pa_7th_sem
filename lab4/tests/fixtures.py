import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.crud import UserCRUD, ProductCRUD, CartItemCRUD
from src.db.models import Base


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer(driver="asyncpg") as postgres:
        yield postgres


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_engine(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_async_engine(db_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def async_session(async_engine):
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            AsyncSessionLocal = sessionmaker(
                connection, class_=AsyncSession, expire_on_commit=False
            )
            session = AsyncSessionLocal()

            yield session

            await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def user_crud(async_session: AsyncSession) -> UserCRUD:
    return UserCRUD(async_session)


@pytest_asyncio.fixture(scope="function")
async def product_crud(async_session: AsyncSession) -> ProductCRUD:
    return ProductCRUD(async_session)


@pytest_asyncio.fixture(scope="function")
async def cart_item_crud(async_session: AsyncSession) -> CartItemCRUD:
    return CartItemCRUD(async_session)
