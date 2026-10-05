from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import Base, WarnRecord
from sqlalchemy import select

DATABASE_URL = "sqlite+aiosqlite:///admin_bot.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database Layer Initialized")

async def add_warn(user_id: int, chat_id: int) -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(WarnRecord).where(
                    WarnRecord.user_id == user_id, 
                    WarnRecord.chat_id == chat_id
                )
            )
            record = result.scalar_one_or_none()
            
            if not record:
                record = WarnRecord(user_id=user_id, chat_id=chat_id, warns_count=1)
                session.add(record)
            else:
                record.warns_count += 1
                
            return record.warns_count

async def reset_warns(user_id: int, chat_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(WarnRecord).where(
                    WarnRecord.user_id == user_id, 
                    WarnRecord.chat_id == chat_id
                )
            )
            record = result.scalar_one_or_none()
            if record:
                await session.delete(record)
