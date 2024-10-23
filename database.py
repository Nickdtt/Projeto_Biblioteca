from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = "postgresql+asyncpg://postgres.glsiiayhqzfxgipxukrr:Fp3ItmfZFcCYChfY@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(bind= engine, autoflush=False, expire_on_commit= False)

Base = declarative_base()

