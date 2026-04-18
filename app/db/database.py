from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine_args = {}
# SQLite requires check_same_thread=False
if settings.database_url.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

# Đối với PostgreSQL (như Neon), SQLAlchemy tự xử lý việc pool connections
engine = create_engine(settings.database_url, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

# Trình quản lý Dependency cung cấp Session cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
