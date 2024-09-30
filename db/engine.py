from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
engine = create_async_engine(f"postgresql+asyncpg://postgres:147896325@localhost:5432/test2", echo=True)#сделать конфиги
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class DBContext:

    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    # try:
        yield SessionLocal
    # except SQLAlchemyError as e:
    #     print(e)
