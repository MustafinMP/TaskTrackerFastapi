from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_NAME_TEST, \
    DB_PORT_TEST


class SqlAlchemyBase(AsyncAttrs, DeclarativeBase):
    ...


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False)

SessionLocal: async_sessionmaker = async_sessionmaker(engine)


def create_session() -> async_sessionmaker[AsyncSession]:
    """Return a new database session.

    :return: new database session object.
    """

    global SessionLocal
    return SessionLocal()
